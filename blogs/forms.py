from django import forms

from .models import BlogPost, PostComment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '', 'text': ''}

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}