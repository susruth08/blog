from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,logout as auth_logout,login as auth_login
from posts.models import Post
from responses.models import Response
from comments.models import Comment
from django.db.models import Max
from django.contrib import messages



def index(request):
    context = {}
    #shows all posts along with the author
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {"user": request.user, "posts": posts }
    else:
        posts = Post.objects.all()
        context = { "posts": posts }

    return render(request, 'blog/index.html', context)

def login(request):
    #check for loginn if user exists log in else return error message
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Invalid Login')
            return render(request, 'blog/login.html')
    else:
        context = {}
        return render(request, 'blog/login.html', context)

def register(request):
    context = {}
    print("register")
    #register user for uniuq values of username and email
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).count() > 0:
            messages.warning(request, 'Username taken')
        elif User.objects.filter(email=email).count() > 0:
            messages.warning(request, 'Email taken')
        elif password != password2:
            messages.warning(request, 'Passwords Do Not Match')
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
    return render(request, 'blog/register.html', context)

def log_out(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('index')

def dashboard(request):
    context = {}
    return render(request, 'blog/dashboard.html', context)

def my_blogs(request):
    context = {}
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)
        context["posts"] = posts
    return render(request, 'blog/my_blogs.html', context)

def analytics(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)

        likes = Response.objects.filter(post__in=posts, liked=True, disliked=False).values('post')
        likes = [like['post'] for like in likes]
        if len(likes) > 0:
            max_likes_post = max(likes,key=likes.count)
            max_likes_post = Post.objects.get(id=max_likes_post)
        else:
            max_likes_post =None
        dislikes = Response.objects.filter(post__in=posts, liked=False, disliked=True).values('post')
        dislikes = [dislike['post'] for dislike in dislikes]
        if len(dislikes) > 0:
            max_dislikes_post = max(dislikes,key=dislikes.count)
            max_dislikes_post = Post.objects.get(id=max_dislikes_post)
        else:
            max_dislikes_post = None

        comments = Comment.objects.filter(post__in=posts).values('post')
        comments = [c['post'] for c in comments]
        if len(comments) > 0:
            max_comments_post = max(comments,key=comments.count)
            max_comments_post = Post.objects.get(id=max_comments_post)
        else:
            max_comments_post=None

        if posts:
            id = posts.values('views', 'id').annotate(Max('views')).first()['id']
            max_views_post = Post.objects.get(id=id)
        else:
            max_views_post = None



        context = {
        "max_likes_post": max_likes_post,
        "max_dislikes_post": max_dislikes_post,
        "max_comments_post": max_comments_post,
        "max_views_post": max_views_post
        }

    return render(request, 'blog/analytics.html', context)
