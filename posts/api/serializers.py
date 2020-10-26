from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comments
from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
         'title',
         'content',
         'publish',
        ]


post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        # lookup_field is to be the primary key but we used slug hence.
        lookup_field='slug'
    )

class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'user',
         'title',
         'id',
         'content',
         'html',
         'publish',
         'slug',
         'image',
         'comments',
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self,obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        c_qs = Comments.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    url = post_detail_url
    class Meta:
        model = Post
        fields = [
         'url',
         'user',
         'title',
         'content',
         'publish',
        ]


