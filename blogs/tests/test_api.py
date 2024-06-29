from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogTests(APITestCase):

    def test_get(self):
        user = User.objects.create(username='test')
        user2 = User.objects.create(username='test2')
        blog_1 = Blog.objects.create(title='Test1', article='test', owner=user)
        blog_2 = Blog.objects.create(title='Test2', article='test2', owner=user2)
        url = reverse('blog-list')
        response = self.client.get(url)
        serializer_data = BlogSerializer([blog_1, blog_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
