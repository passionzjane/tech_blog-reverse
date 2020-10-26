import random
import string

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.conf import settings

# Create your models here.
from django.urls import reverse
from markdown_deux import markdown
from comments.models import Comments
from .utils import get_read_time


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


#class PostManager(models.Manager):
    #def all(self, *args, **kwargs):
        #Post.objecs.all() = super(PostManager, self).all()
        #return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
                              height_field='height_field', width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    #objects = PostManager()

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)+ '-' + id_generator()
        super(Post, self).save(*args, **kwargs)




    def __str__(self):
        return self.title

    def count_time(self):
        return get_read_time(self.get_markdown())

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
        #return "/posts/%s/"%(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        content_type = ContentType.objects.get_for_model(Post)
        obj_id = self.id
        return Comments.objects.filter(content_type=content_type, object_id=obj_id)

    @property
    def get_content_type(self):
        instance = self
        return ContentType.objects.get_for_model(Post)
"""
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)

"""