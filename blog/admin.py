"""
    Blogアプリ
    admin 用の設定

    Filename   admin.py
    Date: 2022.4.21
    Written by Takato Suzuki

"""
from django.contrib import admin
from .models import Post

admin.site.register(Post)
