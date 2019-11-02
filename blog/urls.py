"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import index, login,register, log_out, dashboard,my_blogs, analytics
from django.urls import path,include
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^login/$', login, name="login"),
    url(r'^log_out/$', log_out, name="log_out"),
    url(r'^register/$', register, name="register"),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    path('posts/', include('posts.urls', namespace="posts")),
    path('comments/', include('comments.urls', namespace="comments")),
    url(r'^my_blogs/$', my_blogs, name="my_blogs"),
    url(r'^analytics/$', analytics, name="analytics"),

]
