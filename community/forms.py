from django.forms import ModelForm
from .models import Article, Comment
from django import forms


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'name', 'contents']  # models.py 에서 만든 필드명(변수 이름)

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 30%', 'placeholder': '제목을 입력하세요.'}
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 30%', 'placeholder': '이름을 입력하세요.'}
            ),
            'contents': forms.Textarea(
                attrs={'class': 'form-control', 'style': 'width: 30%', 'placeholder': '내용을 입력하세요.'}
            ),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'comment_user', 'comment_textfield']
        widgets = {
            'comment_textfield': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': '내용을 입력하세요.'}
            ),
        }
