"""
    Blogアプリ
    viewのテスト

    Filename   test_views.py
    Date: 2023.5.13
    Written by Takato Suzuki

"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post

User = get_user_model()

class PostDetailViewTests(TestCase):
    """
        PostDetailViewのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() # テスト用のクライアント

        # ユーザー作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username,password=self.password)

        self.username2 = 'bar@hoge.com'
        self.password2 = 'secret'
        user2 = User.objects.create_user(username=self.username2,password=self.password2)

        # 下書きキ記事作成
        self.post = Post.objects.create(author=user,title="test",text="test")

        # 公開記事作成
        self.post2 = Post.objects.create(author=user,title="test2",text="test2")
        self.post2.publish()

        #別ユーザの記事
        self.post3 = Post.objects.create(author=user2, title="test3",text="test3")

        # 詳細ページのパスを作成
        # 下書き記事
        self.path = reverse('blog:post_detail',args=(self.post.id,))
        # 公開記事
        self.path2 = reverse('blog:post_detail',args=(self.post2.id,))
        #別ユーザの記事
        self.path3 = reverse('blog:post_detail', args=(self.post3.id,))

    def test_mypost_logged_in(self):
        """ログイン済みで自分の下書き記事"""
        # ユーザを作成し、ログイン
        self.client.login(username=self.username,password=self.password)

        # テスト対象を実行
        res = self.client.get(self.path)

        #自分の記事は閲覧可能
        self.assertEqual(res.status_code, 200)

    def test_not_mypost_logged_in(self):
        """ログイン済みで他人の下書き記事"""
        #ユーザを作成し、ログイン
        self.client.login(username=self.username,password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path3)

        #他人の下書き記事は閲覧不可
        self.assertEqual(res.status_code, 403)

    def test_superuser_logged_in(self):
        """ログイン済みでスーパーユーザーが他人の下書き記事を閲覧"""
        #スーパーユーザ
        username = "super@hoge.com"
        password = "test"
        superuser = User.objects.create_superuser(username=username,password=password)

        #ユーザを作成し、ログイン
        self.client.login(username=username,password=password)

        #テスト対象を実行
        res = self.client.get(self.path3)

        #スーパーユーザがログインする場合は常に閲覧可能
        self.assertEqual(res.status_code,200)

    def test_not_published_not_logged_in(self):
        """ログインしていない下書き記事の場合のテスト"""
        # テスト対象を実行
        res = self.client.get(self.path)

        # 記事は見られない
        self.assertEqual(res.status_code, 403)

    def test_published_not_logged_in(self):
        """ログインしていない公開記事の場合のテスト"""
        # テスト対象を実行
        res = self.client.get(self.path2)

        # 記事は見られる
        self.assertEqual(res.status_code, 200)

class PostReviewListViewTests(TestCase):
    """
        下書き一覧ページのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テストのクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username,password=self.password)

        #下書き記事作成
        self.post = Post.objects.create(author=user, title="test",text="test")

        #下書き一覧ページ
        self.path = reverse('blog:post_review')

    def test_mypost_logged_in(self):
        """ログイン済みで自分の下書き一覧を表示"""
        #ユーザを作成し、ログイン
        self.client.login(username=self.username,password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path)

        #自分の記事は閲覧可能
        self.assertEqual(res.status_code, 200)

        self.assertQuerysetEqual(
            res.context['posts'],['<Post: test>']
        )
        self.assertContains(res, self.post.title)

    def test_mypost_not_logged_in(self):
        """ログイン済みで自分の下書き一覧を表示"""
        #テスト対象を実行
        res = self.client.get(self.path)

        #自分の記事は閲覧可能
        self.assertEqual(res.status_code,302)

class PostCreateViewTests(TestCase):
    """
        記事作成ページのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テスト用のクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username, password=self.password)

        #記事追加
        self.path = reverse('blog:post_add')

    def test_logged_in(self):
        """ログインしたときに表示"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path)

        #表示可能
        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        """ログインしていないときはリダイレクト"""
        #テスト対象を実行
        res = self.client.get(self.path)

        #ログインページにリダイレクト
        self.assertEqual(res.status_code, 302)

    def test_post_null(self):
        """空のデータで記事作成"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        data = {}
        res = self.client.post(self.path, data=data)
        #成功しない場合は同じページを表示
        self.assertEqual(res.status_code, 200)

    def test_post_with_data(self):
        """記事を登録する"""

        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        data = {
            'title': 'こんにちは',
            'text': 'ようこそ',
        }
        res = self.client.post(self.path, data=data)
        #成功すればリダイレクト
        self.assertEqual(res.status_code, 302)

class PostListViewTests(TestCase):
    """
        記事一覧ページのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テスト用のクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username, password=self.password)

        # 記事作成
        self.post1 = Post.objects.create(author=user,title="test1",text="test1")
        self.post1.publish()
        self.post2 = Post.objects.create(author=user,title="test2",text="test2")
        self.post2.publish()

        #一覧取得
        self.path = reverse('blog:post_list')

    def test_logged_in(self):
        """ログインしたときに表示"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path)

        #表示可能
        self.assertEqual(res.status_code, 200)
        #print(res.context)
        # リストを表示
        self.assertQuerysetEqual(
            res.context['post_list'],['<Post: test1>', '<Post: test2>']
        )
        self.assertContains(res, self.post1.title)
        self.assertContains(res, self.post2.title)

    def not_logged_in(self):
        """ログインしていない"""
        #テスト対象を実行
        res = self.client.get(self.path)

        #表示可能
        self.assertEqual(res.status_code, 200)

    def test_post_list_serach(self):
        """検索する一覧表示"""
        #test1を検索し、それが表示されるかどうか
        data = {
                'key_word' : 'test1'
        }

        #テスト対象を実行
        res = self.client.get(self.path, data=data)

        # リストを表示
        self.assertQuerysetEqual(
            res.context['post_list'],['<Post: test1>']
        )

class PublishRedirectViewTests(TestCase):
    """
        公開ボタンのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テスト用のクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username, password=self.password)

        # 記事作成
        self.post1 = Post.objects.create(author=user,title="test1",text="test1")
        self.post1.publish()

        #パスを作成
        self.path1 = reverse('blog:publish', args=(self.post1.id,))
        self.path2 = reverse('blog:publish', args=(1001,)) #適当な記事番号

    def test_logged_in(self):
        """ログインして公開"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path1)

        #表示可能
        self.assertEqual(res.status_code, 302)

    def not_logged_in(self):
        """ログインしていない"""
        #ログインせずに実行した場合はログインページに飛ぶ
        #テスト対象を実行
        res = self.client.get(self.path)

        #表示可能
        self.assertEqual(res.status_code, 302)

    def test_not_found_logged_in(self):
        """リソースがない"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path2)

        #表示不可
        self.assertEqual(res.status_code, 404)

class PostUpdateViewTests(TestCase):
    """
        公開ボタンのテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テスト用のクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username, password=self.password)

        # 記事作成
        self.post1 = Post.objects.create(author=user,title="test1",text="test1")
        self.post1.publish()

        #パスを作成
        self.path1 = reverse('blog:post_update', args=(self.post1.id,))
        self.path2 = reverse('blog:post_update', args=(1001,)) #適当な記事番号


    def test_logged_in(self):
        """ログインして公開"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path1)

        #表示可能
        self.assertEqual(res.status_code, 200)

    def not_logged_in(self):
        """ログインしていない"""

        #テスト対象を実行
        res = self.client.get(self.path)

        #ログインせずに実行した場合はログインページに飛ぶ
        self.assertEqual(res.status_code, 302)

    def test_update_post(self):
        """記事を変更"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        data = {
            'title': 'こんにちは',
            'text': 'ようこそ',
        }
        res = self.client.post(self.path1, data=data)

        #表示可能
        self.assertEqual(res.status_code, 302)

    def test_not_found_logged_in(self):
        """リソースがない"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path2)

        #表示不可
        self.assertEqual(res.status_code, 404)

class PostDeleteViewTests(TestCase):
    """
        記事削除のテスト
    """
    def setUp(self):
        super().setUp()
        self.client = Client() #テスト用のクライアント

        #ユーザ作成
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username, password=self.password)

        # 記事作成
        self.post1 = Post.objects.create(author=user,title="test1",text="test1")
        self.post1.publish()

        #パスを作成
        self.path1 = reverse('blog:post_delete', args=(self.post1.id,))
        self.path2 = reverse('blog:post_delete', args=(1001,)) #適当な記事番号

    def test_logged_in(self):
        """ログインして公開"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path1)

        #表示可能
        self.assertEqual(res.status_code, 200)

    def not_logged_in(self):
        """ログインしていない"""
        #ログインせずに実行した場合はログインページに飛ぶ
        #テスト対象を実行
        res = self.client.get(self.path)

        #ログインせずに実行した場合はログインページに飛ぶ
        self.assertEqual(res.status_code, 302)

    def test_delete_post(self):
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.post(self.path1)

        #削除成功
        self.assertEqual(res.status_code, 302)

    def test_not_found_logged_in(self):
        """リソースがない"""
        #ユーザログイン
        self.client.login(username=self.username, password=self.password)

        #テスト対象を実行
        res = self.client.get(self.path2)

        #表示不可
        self.assertEqual(res.status_code, 404)
