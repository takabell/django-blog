"""
	Accountsアプリ
	URL定義

	Filename   urls.py
	Date: 2020.2.16
	Written by Takato Suzuki
"""

from django.urls import path
from . import views

app_name = 'accounts'   # アプリケーション名
urlpatterns = [
	#'prfile'はURLリンクのパスを書いている。
	path('profile/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
	path('profile/update/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
	#PasswordChangeViewとPasswordChangeDoneViewはDjangoのアカウント機能にあるやつ
	path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done/', views.PasswordChangeDoneView.as_view(), name=('password_change_done')),
	path('create/',views.UserCreate.as_view(), name='user_create'),
]
