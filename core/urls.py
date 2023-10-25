from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('profilepage', views.profilepage, name='profilepage'),
    path('upload',views.upload,name='upload'),
    path('like-post',views.like_post, name='like-post'),
    path('search', views.search, name='search'),
    path('post_detail/<str:post_id>/', views.post_detail, name='post_detail'),
    ] 