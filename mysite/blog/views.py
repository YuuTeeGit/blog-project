from django.shortcuts import render
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                    DeleteView,CreateView,
                                    UpdateView,DetailView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):#https://docs.djangoproject.com/ja/3.0/topics/db/queries/#field-lookups
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    #LoginRequiredMixin:ログインを促す仕組み
    #https://qiita.com/hayata-yamamoto/items/d0305942199acd63b7c9
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteview(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')#urlをnameで指定できる。

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):#未公開の記事を返すクエリ
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')