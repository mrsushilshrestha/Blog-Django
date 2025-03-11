from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from blog.models import Post, Comment, Like
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm, UserProfileForm

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'frontend/home.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    
    # Check if the user has liked the post
    user_liked_post = False
    if request.user.is_authenticated:
        user_liked_post = Like.objects.filter(post=post, user=request.user).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'frontend/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked_post': user_liked_post
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'frontend/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'frontend/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'frontend/post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        messages.info(request, 'Post unliked!')
    else:
        messages.success(request, 'Post liked!')
    
    return redirect('post_detail', slug=slug)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'frontend/profile.html', {
        'form': form,
        'user_posts': user_posts
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})
