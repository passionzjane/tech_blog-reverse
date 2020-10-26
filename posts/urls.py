from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('post/create/', views.post_create),
    path('post/<slug:slug>/', views.post_detail, name='detail'),
    path('post/<slug:slug>/edit/', views.post_update, name='update'),
    path('post/<slug:slug>/delete/', views.post_delete),
]
