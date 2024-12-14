"""
	template tagの拡張

	Filename   blog_extras.py
	Date: 2020.3.6
	Written by Shinsuke Kobayashi

"""
from django import template
from django.shortcuts import resolve_url
from urllib import parse

register = template.Library()# テンプレートライブラリに追加するための記述

@register.simple_tag
def get_return_link(request):
	"""
		一つ前のページのURLを取得するテンプレートタグ
	"""
	top_page = resolve_url('blog:post_list')		# 記事一覧
	referer = request.environ.get('HTTP_REFERER')   # 前ページのURLを取得する

	if referer:
		# 前ページのURLがある場合、前ページが自分のサイト内であればそこに戻す。
		parse_result = parse.urlparse(referer)
		if request.get_host() == parse_result.netloc:
			return referer
	# なければトップページ
	return top_page

@register.simple_tag
def url_replace(request, field, value):
	"""
		GETパラメータの一部を置き換える
	"""
	url_dict = request.GET.copy()
	url_dict[field] = str(value)
	return url_dict.urlencode()
