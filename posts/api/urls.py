from django.urls import path
from posts.api.views import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/edit/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug:slug>/delete/', PostDeleteAPIView.as_view(), name='delete')
]
