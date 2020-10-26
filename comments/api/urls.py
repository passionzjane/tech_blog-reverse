from django.urls import path

from comments.views import comment_thread
from posts import views
from .views import (
CommentCreateAPIView,
CommentDetailApiView,
CommentListAPIView
)

app_name = 'comments'

urlpatterns = [
path('', CommentListAPIView.as_view(), name='list'),
path('create/', CommentCreateAPIView.as_view(), name='create'),
path('<int:pk>/', CommentDetailApiView.as_view(), name='thread'),
#path('/<int:id>/delete/', comment_delete, name="delete"),
]
