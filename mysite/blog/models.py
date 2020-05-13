from django.db import models
from django.utils import timezone #時刻の取得、タイムゾーンはsettings.pyの設定に依存
from django.urls import reverse #Django の urls に設定された名前をパラメータとして渡すと、URLを返す。
# Create your models here.

class Post(models.Model):#Postモデルのテーブルを設定
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #authアプリのUser機能を使う
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    def __str__(self):#管理画面で表示される文字列を定義
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)#Postモデルのコメントと紐付け
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
 
    def get_absolute_url(self):
        return reverse('post_list')
    
    def __str__(self):
        return self.text