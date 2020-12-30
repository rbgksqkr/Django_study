from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    contents = models.TextField()
    cdate = models.DateTimeField(auto_now_add=True)
    # body = RichTextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_user = models.CharField(max_length=20)
    comment_textfield = models.TextField()
    comment_thumbnail_url = models.CharField(max_length=300)

    def __str__(self):
        return self.comment_textfield

# class User(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)


