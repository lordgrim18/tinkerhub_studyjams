from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<str:pk>/', views.blog, name='blog'),

    path('create-blog/', views.createBlog, name='create-blog'),
    path('update-blog/<str:pk>/', views.updateBlog, name='update-blog'),
    path('delete-blog/<str:pk>/', views.deleteBlog, name='delete-blog'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),

]