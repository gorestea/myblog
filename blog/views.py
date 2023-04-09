from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import Group
from .forms import *
from .utils import *

class PostHome(DataMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category')



class AddPage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, CreateView):
    permission_required = 'blog.add_post'
    form_class = AddPostForm
    template_name = 'addpage.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание поста')
        return dict(list(context.items()) + list(c_def.items()))

# @login_required
# def access(request):
#     if request.user.is_superuser:
#         if request.method == 'POST':
#             form = AddPostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('home')
#         else:
#             form = AddPostForm()
#     else:
#         raise Http404('Страницы не существует')
#     return render(request, 'addpage.html', {'form': form})

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post_id=post.id)
    categories = Category.objects.annotate(Count('post'))
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddComment(request.POST)
            if form.is_valid():
                result = form.cleaned_data
                new = Comment(
                    post=Post.objects.get(slug=post_slug),
                    user=User.objects.get(username=request.user.username),
                    text=result['text']
                )
                new.save()
                return redirect(f'/post/{post_slug}')
        else:
            form = AddComment()
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'title': post.title,
            'category': categories
        }
        return render(request, 'post.html', context)
    else:
        context = {
            'post': post,
            'comments': comments,
            'title': post.title,
            'category': categories
        }
        return render(request, 'post.html', context)

class PostCategory(DataMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      category_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Users')
        user.groups.add(group)
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def send_email(request):
    form = GetEmail()
    categories = Category.objects.annotate(Count('post'))
    if request.method == 'POST':
        form = GetEmail(request.POST)
        if form.is_valid():
            data = {
                'name': request.user.username,
                'email': request.user.email,
                'text': form.cleaned_data['text'],
            }
            html_body = render_to_string('email.html', data)
            msg = EmailMultiAlternatives(subject='Вопрос от пользователя блога', to=['lyblygambit@yandex.ru'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
        return redirect('/')
    return render(request, 'contact.html', {'form': form, 'title': 'Обратная связь', 'category': categories})