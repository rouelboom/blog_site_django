from http import HTTPStatus

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment, Follow


def index(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, settings.PAGINATOR_LENTH)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
                  'page': page,
                  'paginator': paginator
                  })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()

    paginator = Paginator(posts, settings.PAGINATOR_LENTH)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'group.html', {
                  'group': group,
                  'page': page,
                  'paginator': paginator
                  })


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:index')
    return render(request, 'new_post.html', {
                  'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()

    paginator = Paginator(posts, settings.PAGINATOR_LENTH)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    followers = Follow.objects.filter(user=author).all()
    following = Follow.objects.filter(author=author).all()

    context = {'author': author,
               'page': page,
               'paginator': paginator,
               'followers': followers,
               'following': following}
    if request.user.is_authenticated:
        context['is_user_follow'] = Follow.objects.filter(user=request.user,
                                                          author=author)

    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.username == username:
        comments = Comment.objects.filter(post=post).all()
        form = CommentForm()
        return render(request, 'post.html', {'author': post.author,
                                             'post': post,
                                             'comments': comments,
                                             'form': form})
    return HttpResponse(HTTPStatus.NOT_FOUND)


@login_required
def post_edit(request, username, post_id):
    edited_post = get_object_or_404(Post, id=post_id)
    if not edited_post.author.username == username:
        return HttpResponse(HTTPStatus.NOT_FOUND)

    if not edited_post.author == request.user:
        return redirect('posts:post', username, post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=edited_post)
    if form.is_valid():
        edited_post.save()
        return redirect('posts:post', username, post_id)
    return render(request, 'new_post.html', {
                  'form': form,
                  'post': edited_post})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=username)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = author
        comment.save()
        return redirect('posts:post', username, post_id)
    return redirect('posts:post', username, post_id)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)

    paginator = Paginator(post_list, settings.PAGINATOR_LENTH)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'follow.html', {
                  'page': page,
                  'paginator': paginator
                  })


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user == author:
        return redirect('posts:profile', username)

    Follow.objects.get_or_create(
        user=request.user,
        author=author,
    )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username)
