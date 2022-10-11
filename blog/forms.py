"""
	Blogアプリ
	フォームクラス

	Filename   forms.py
	Date: 2022.10.11
	Written by Takato Suzuki

"""
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
	"""
		記事登録画面用のフォーム
		title  : ブログのタイトル
		text   : ブログ本文
	"""
	class Meta:
		#  モデルクラスを指定
		model = Post
		#  モデルフィールドを指定
		fields = ("title", "text")
		labels = {
			'title': 'タイトル',
			'text': '本文',
		}
