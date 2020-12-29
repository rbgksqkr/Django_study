from django.db import models


# Create your models here.
class Article(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    contents = models.TextField()
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class User(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)


