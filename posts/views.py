from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone
from urllib.parse import quote_plus

from comments.forms import CommentForms
from posts.forms import PostForm
from posts.models import Post
from comments.models import Comments
from django.contrib import messages
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def post_list(request):  # list item
    today = timezone.now().date()
    posts = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())
    if request.user.is_staff or request.user.is_superuser:
        posts = posts.all()

    post = request.GET.get("post")
    if post:
        posts = posts.filter(
            Q(title__icontains=post) |
            Q(content__icontains=post) |
            Q(user__first_name__icontains=post) |
            Q(user__last_name__icontains=post)
        ).distinct()
    # Pagination
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # endpaginition

    context = {
        "posts": posts,
        "title": "List",
        "today": today,
    }

    return render(request, 'posts/post_list.html', context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Post was successfully created')
        # message success
        return redirect('posts:detail', post.slug)
    # if request.method == "POST":
    # print(request.POST)
    # print(request.POST.get("content"))
    # print(request.POST.get("title"))
    context = {
        "form": form,
    }
    return render(request, 'posts/post_form.html', context)


def post_detail(request, slug):  # retrive
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.content)

    initial_data = {
        "content_type": 'post',
        "object_id": post.id
    }
    form = CommentForms(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        # print(form.cleaned_data)
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        # print(content_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = request.POST.get("parent_id")
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comments.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comments.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "post": post,
        "share_string": share_string,
        "comment_form": form,
    }
    return render(request, 'posts/post_detail.html', context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        # message success
        messages.success(request, 'Post was successfully edited', extra_tags="some-tags")
        # link  = '/post/'+post.id
        return redirect('posts:detail', post.slug)

    context = {
        "title": post.title,
        "post": post,
        "form": form,
    }
    return render(request, 'posts/post_form.html', context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, 'Post was successfully created')
    return redirect('posts:list')
