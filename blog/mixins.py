"""
    Blogアプリ

    Filename   mixins.py
    Date: 2023.5.13
    Written by Takato Suzuki

"""
from typing import Optional
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import get_object_or_404

class CheckPermissionMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        """
            記事が公開されている場合はTrue
            それ以外はユーザーが一致する場合とスーパーユーザーの場合許可する
        """
        # 対象となる記事を取得
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # 記事が公開なら True
        if post.published_date:
            return True

        # 下書きならユーザー一致かスーパーユーザの場合
        user = self.request.user
        return user.pk == post.author.pk or user.is_superuser
