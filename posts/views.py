from django.shortcuts import render
from .models import Post
from comments.models import Comment
from responses.models import Response
from django.http import HttpResponse
from responses.models import Response
from django.contrib.auth.models import User


# Create your views here.
def new(request):
    print(request.user)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        author = request.user
        Post.objects.create(title=title, description=description, author=author)
    return render(request, 'posts/new.html')

def show(request, *args, **kwargs):
    id = kwargs['id']
    post = Post.objects.get(id=id)
    post.views = post.views + 1
    post.save()
    comments = Comment.objects.filter(post=post)
    if request.user.is_authenticated:
        response = Response.objects.filter(post=post, user=request.user).first()
    else:
        response = ""
    liked_by = Response.objects.filter(post=post, liked=True,disliked=False).values('user')
    liked_by = set([l['user'] for l in liked_by])
    liked_by = User.objects.filter(id__in=liked_by).values('username')

    disliked_by = Response.objects.filter(post=post, liked=False,disliked=True).values('user')
    disliked_by = set([l['user'] for l in disliked_by])

    disliked_by = User.objects.filter(id__in=disliked_by).values('username')

    context={
    "post": post,
    "comments": comments,
    "response": response,
    "liked_by": liked_by,
    "disliked_by": disliked_by

    }
    return render(request, 'posts/show.html', context=context)

def like(request):
    if request.method == 'POST':
        id = request.POST['id']
        print(id)
        user = request.user
        post = Post.objects.filter(id=id)
        response = Response.objects.filter(user=user, post=post.first()).first()
        if response:
            response.liked = True
            response.disliked = False
            response.save()
            return HttpResponse(status=200)
        else:
            response = Response.objects.create(liked=True, disliked=False,user=user,post=post.first())
            return HttpResponse(status=200)

    return HttpResponse(status=400)

def dislike(request):
    if request.method == 'POST':
        id = request.POST['id']
        print(id)
        user = request.user
        post = Post.objects.filter(id=id)
        response = Response.objects.filter(user=user, post=post.first()).first()
        if response:
            response.liked = False
            response.disliked = True
            response.save()
            return HttpResponse(status=200)
        else:
            response = Response.objects.create(liked=False, disliked=True,user=user,post=post.first())
            return HttpResponse(status=200)
    return HttpResponse(status=400)
