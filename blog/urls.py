from django.urls import path
from .views import *

urlpatterns = [
    path('', PostHome.as_view(), name='home'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', send_email, name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:cat_slug>/', PostCategory.as_view(), name='category')
]