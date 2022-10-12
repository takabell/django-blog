"""
	Blogアプリ
	表示用の機能作成

	Filename   views.py
	Date: 2022.9.27
	Written by Shinsuke Kobayashi

"""
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import View,DetailView, CreateView, RedirectView, UpdateView, DeleteView
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(View):
	def get(self, request, *args, **kwargs):
		"""
			Get request 用の処理
			ブログ記事一覧を表示する
		"""
		context = {}
		#  記事データを取得
		#'-published_date'は「-」は降順の意味
		posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
		context['posts'] = posts
		return render(request, "blog/post_list.html", context)

post_list = PostListView.as_view()

class PostDetailView(DetailView):
	model = Post
	template_name = "blog/post_detail.html"

post_detail = PostDetailView.as_view()

class PostCreateView(LoginRequiredMixin, CreateView):
	"""
		ブログ記事作成用のビュー
	"""
	model = Post							# 対象とするモデル
	form_class = PostForm				   # 使用するフォームクラス
	template_name = "blog/post_add.html"	# テンプレート

	def form_valid(self, form):
		# ユーザを追加
		form.instance.author = self.request.user

		return super().form_valid(form)

	def get_success_url(self):
		""" 詳細画面にリダイレクトする """
		return reverse('blog:post_detail', args=(self.object.id,))

class PostReviewListView(LoginRequiredMixin, View):
	"""
		下書き一覧のページ
	"""
	def get(self, request, *args, **kwargs):
		"""
			ブログの下書き記事一覧を表示する
		"""
		context = {}
		#  記事データを取得
		posts = Post.objects.filter(author=self.request.user, published_date__isnull=True).order_by('create_date')
		context['posts'] = posts
		return render(request, "blog/review_list.html", context)

class PublishRedirectView(LoginRequiredMixin, RedirectView):
	"""
		詳細ページでpublishに変更するボタンを押したときにリダイレクトして一覧に戻す
	"""
	pattern_name = 'blog:post_detail'

	def get_redirect_url(self, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['pk'])
		post.publish()
		return super().get_redirect_url(*args, **kwargs)

class PostUpdateView(LoginRequiredMixin, UpdateView):
	"""
		変更ページのビュー
	"""
	model = Post
	form_class = PostForm
	template_name = 'blog/post_update.html'

	# 更新が終了した時に表示する
	def get_success_url(self):
		"""詳細画面にリダイレクトする"""
		#object.idは記事番号
		#reverseはURLを逆引きする関数
		return reverse('blog:post_detail', args=(self.object.id,))

class PostDeleteView(LoginRequiredMixin, DeleteView):
	"""
		削除用のビュー
	"""
	model = Post
	template_name = 'blog/post_delete.html'
	def get_success_url(self):
		"""一覧ページにリダイレクトする"""
		return reverse('blog:post_list')
