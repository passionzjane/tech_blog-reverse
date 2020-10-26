from rest_framework.generics import (
CreateAPIView,
DestroyAPIView,
ListAPIView,
RetrieveAPIView,
RetrieveUpdateAPIView,
UpdateAPIView
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import (
AllowAny,
IsAuthenticated,
IsAdminUser,
IsAuthenticatedOrReadOnly,
)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.filters import (
SearchFilter,
OrderingFilter
)

from django.db.models import Q
from comments.models import Comments
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Comments.objects.filter(id__gte=0)
        comment = self.request.GET.get("comment")
        #q search
        if comment:
            queryset = queryset.filter(
                Q(content__icontains=comment) |
                Q(user__first_name__icontains=comment) |
                Q(user__last_name__icontains=comment)
            ).distinct()
        return queryset

class CommentDetailApiView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comments.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
"""
"""
class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
"""

class CommentCreateAPIView(CreateAPIView):
    queryset = Comments.objects.all()
    #serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.Get.get('type')
        slug = self.request.Get.get('slug')
        parent_id = self.request.Get.get('parent_id', None)
        return create_comment_serializer(
            model_type='model_type',
            slug='slug',
            parent_id=parent_id,
            user=self.request.user
        )
"""
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
"""