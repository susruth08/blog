from django.shortcuts import render,redirect
from posts.models import Post
from comments.models import Comment
# Create your views here.

def create(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST['post_id']
        post = Post.objects.get(id=id)
        comment= request.POST['comment']
        Comment.objects.create(description=comment,user=user, post=post)
        return redirect('posts:show', id=id)
