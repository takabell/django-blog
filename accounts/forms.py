"""
	Accounts　更新フォームの定義

	Filename   forms.py
	Date: 2022.9.27
	Written by Takato Suzuki

"""
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserUpdateForm(ModelForm):
	"""ユーザー情報更新フォーム"""
	class Meta:
		model = User
		fields = ('last_name', 'first_name',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			#'form-control'はbootstrapの属性を追加している。
			field.widget.attrs['class'] = 'form-control'

class UserCreateForm(UserCreationForm):
	"""
		ユーザー作成用のフォーム
	"""
	class Meta(UserCreationForm.Meta):
		#パスワードは指定しなくともデフォルトで追加される。
		fields = ('username', 'email')
