from django.urls import path

from . import views
app_name = "posts"
urlpatterns = [
path('new', views.new, name='new'),
path('show/<int:id>', views.show, name='show'),
path('like', views.like, name='like'),
path('dislike', views.dislike, name='dislike'),

]
