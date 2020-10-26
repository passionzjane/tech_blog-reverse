from rest_framework.generics import (
CreateAPIView,
DestroyAPIView,
ListAPIView,
RetrieveAPIView,
RetrieveUpdateAPIView,
UpdateAPIView
)
from.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.filters import (
SearchFilter,
OrderingFilter
)

from django.db.models import Q

from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
)
from posts.models import Post

from rest_framework.permissions import (
AllowAny,
IsAuthenticated,
IsAdminUser,
IsAuthenticatedOrReadOnly,
)
from .permissions import IsOwnerOrReadOnly


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Post.objects.all()
        post = self.request.GET.get("post")
        #q search
        if post:
            queryset = queryset.filter(
                Q(title__icontains=post) |
                Q(content__icontains=post) |
                Q(user__first_name__icontains=post) |
                Q(user__last_name__icontains=post)
            ).distinct()
        return queryset

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
   # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
