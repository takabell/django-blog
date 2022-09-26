"""
    Blogアプリ
    URL定義

    Filename   urls.py
    Date: 2022.4.21
    Written by Takato Suzuki

"""
from django.urls import path
from . import views

app_name = 'blog'   # アプリケーション名
urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
