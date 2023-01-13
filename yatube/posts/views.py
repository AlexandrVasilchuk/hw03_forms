from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate
from posts.forms import PostForm
from posts.models import Group, Post

user_model = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related(
        'author',
        'group',
    )
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': paginate(request, posts),
        },
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related(
        'author',
        'group',
    )
    return render(
        request,
        'posts/group_list.html',
        {
            'page_obj': paginate(request, posts),
            'group': group,
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(user_model, username=username)
    posts = user.posts.all()
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': paginate(request, posts),
            'author': user,
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
        },
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
            },
        )
    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    is_edit = True
    post = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'is_edit': is_edit,
                'form': form,
            },
        )
    post.save()
    return redirect('posts:post_detail', pk)
