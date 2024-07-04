from unittest import TestCase
from blogs.models import User, Blog
from blogs.serializers import BlogSerializer


class BlogSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test3')
        self.user2 = User.objects.create(username='test2')
        self.blog_1 = Blog.objects.create(title='Test1', article='test', owner=self.user)
        self.blog_2 = Blog.objects.create(title='Test2', article='test2', owner=self.user2)

    def test_ok(self):
        data = BlogSerializer([self.blog_1, self.blog_2], many=True).data
        print(data)
        expected_data = [{
            'title': 'Test1',
            'owner': self.user.id,
            'article': 'test',
            # 'data': datetime.datetime.now().isoformat(),
            'comments': [],
            'likes': []
        }, {
            'title': 'Test2',
            'owner': self.user2.id,
            'article': 'test2',
            'comments': [],
            'likes': []
        }]
        print(expected_data)
        self.assertEqual(expected_data, data)