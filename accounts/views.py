"""
	Accounts　表示部分

	Filename   views.py
	Date: 2022.9.27
	Written by Takato Suzuki

"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, UpdateView
from django.shortcuts import resolve_url
from .forms import UserUpdateForm
from django.contrib.auth.models import User

#UserPassesTestMixin　ユーザがある条件をパスしているかをテストための機能
#同じ処理を２つのビューで追加するために作成
class OnlyYouMixin(UserPassesTestMixin):
	raise_exception = True

	#テストをする関数でUserPassesTestMixinクラスの機能
	def test_func(self):
		"""
			ユーザがページのIDと一致する場合とスーパーユーザの場合許可する
		"""
		user = self.request.user
		return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, DetailView):
	"""
		ユーザの詳細を表示するビュー
	"""
	model = User	#models.pyのクラスを指定するが、今回はDjangoのUserをimportして使っている。
	template_name = 'accounts/user_detail.html'


#CreateViewは新しいオブジェクトを作成する。
#UpdateViewは既存のオブジェクトを変更する
class UserUpdate(OnlyYouMixin, UpdateView):
	"""
		ユーザデータの更新をするためのビュー
	"""
	model = User
	form_class = UserUpdateForm	#forms.pyのクラスを指定する。modelの役割
	template_name = 'accounts/user_form.html'

	def get_success_url(self):
		"""
			更新成功後の表示をする画面。ユーザの詳細を表示する画面に遷移する。
		"""
		return resolve_url('accounts:user_detail', pk=self.kwargs['pk'])
