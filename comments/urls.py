from django.urls import path

from comments.views import comment_thread
from posts import views
from .views import (
comment_thread,
comment_delete
)

app_name = 'comments'

urlpatterns = [
path('/<int:id>/', comment_thread, name='thread'),
path('/<int:id>/delete/', comment_delete, name="delete"),
]
