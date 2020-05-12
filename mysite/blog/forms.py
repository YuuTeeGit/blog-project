from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():#forms.ModelFormクラスに機能を追加
        model = Post
        fields = ('author','title','text')

        widgets = {#それぞれの入力項目の設定
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }
        