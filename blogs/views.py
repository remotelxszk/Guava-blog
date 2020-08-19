from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import BlogPost, PostComment
from .forms import BlogPostForm, PostCommentForm

def check_post_owner(request, post):
    """Allow post owner to edit or return 404."""
    if post.owner != request.user:
        raise Http404

# Create your views here.

def index(request):
    """The home page for Blogs"""
    blog_list = BlogPost.objects.order_by('-date_added')
    paginator = Paginator(blog_list, 4) #4 posts in each page
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    comments = PostComment.objects.all()
    context = {'blogs': blogs, 'comments': comments, 'page': page}
    return render(request, 'blog/index.html', context)

@login_required
def new_post(request):
    """Form for addind new posts."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogPostForm()
    else:
        # POST data submitted; process data.
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('blogs:index'))
    context = {'form': form}
    return render(request, 'blog/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing blog post."""
    post = get_object_or_404(BlogPost, id=post_id)
    check_post_owner(request, post)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current post.
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:view_post',
                                        args=[post_id]))
    context = {'post': post, 'form': form}
    return render(request, 'blog/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    check_post_owner(request, post)
    post.delete()
    return HttpResponseRedirect(reverse('blogs:index'))

def view_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.postcomment_set.order_by('-date_added')
    context = {'blog': post, 'comments': comments}
    return render(request, 'blog/view_post.html', context)

@login_required
def new_comment(request, post_id):
    """Form for adding new comments."""
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostCommentForm()
    else:
        # POST data submitted; process data.
        form = PostCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post_id = post_id
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:view_post',
                                        args=[post_id]))
    context = {'blog': post, 'form': form}
    return render(request, 'blog/new_comment.html', context)

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)
    check_post_owner(request, comment)
    comment.delete()
    return HttpResponseRedirect(reverse('blog:view_post',
                                        args=[post_id]))

@login_required
def edit_comment(request, post_id, comment_id):
    """Edit an existing blog post."""
    post = get_object_or_404(PostComment, id=comment_id)
    check_post_owner(request, post)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current post.
        form = PostCommentForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostCommentForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:view_post',
                                        args=[post_id]))
    context = {'blog_id': post_id, 'comment': post, 'form': form}
    return render(request, 'blog/edit_comment.html', context)
