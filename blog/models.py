"""
    Blogアプリ
    データモデル

    Filename models.py
    Date:2022.4.21
    Written by Takato Suzuki

"""
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    """
        ブログ記事クラス

        author  : 作者（Djangoのユーザモデル）
        title   :ブログのタイトル
        text    :ブログ本文
        create_date:作成日
        published_date:公開日

    """
    # フィールドの定義
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
