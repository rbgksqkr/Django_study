from django.forms import ModelForm
from community.models import *


class Form(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'title', 'contents']  # models.py 에서 만든 필드명(변수 이름)


# class UserDataForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
