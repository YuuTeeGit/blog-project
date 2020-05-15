from django.shortcuts import render,get_object_or_404,redirect
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

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')#urlをnameで指定できる。

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):#未公開の記事を返すクエリ
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


################################################
################################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)

@login_required #Viewをログイン済みのユーザーにのみ制限する#https://wonderwall.hatenablog.com/entry/2018/03/25/180000
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)#ページが存在しなければ404を返すショートカット
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():            
            comment = form.save(commit=False)
            comment.post = post#postの紐付け
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = CommentForm()

    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.approve()
    return redirect('blog:post_detail',pk=post_pk.pk)#COmmentModelのpost.pkを参照

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()#Modelクラスに元々あるもの
    return redirect('blog:post_detail',pk=post_pk)
