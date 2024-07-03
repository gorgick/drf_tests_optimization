from django.contrib.auth.models import User
from django.db.models import Prefetch, Count, F
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer


class BlogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user2 = User.objects.create(username='test2')
        self.user3 = User.objects.create(username='test3')
        self.blog_1 = Blog.objects.create(title='Test1', article='test', owner=self.user)
        self.blog_2 = Blog.objects.create(title='Test2', article='test2', owner=self.user2)
        self.blog_3 = Blog.objects.create(title='Test2', article='test3', owner=self.user3)

    def test_get(self):
        url = reverse('blog-list')
        response = self.client.get(url)
        blogs = Blog.objects.all().prefetch_related(Prefetch('comments', queryset=Comment.objects.all().annotate(
            owner_name=F('owner__username')))).prefetch_related('likes').annotate(
            author_name=F('owner__username')).annotate(likes_count=Count('likes'))
        serializer_data = BlogSerializer(blogs, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_search(self):
        url = reverse('blog-list')
        response = self.client.get(url, data={'search': 'Test2'})
        blogs = Blog.objects.filter(id__in=[self.blog_2.id, self.blog_3.id]).prefetch_related(
            Prefetch('comments', queryset=Comment.objects.all().annotate(
                owner_name=F('owner__username')))).prefetch_related('likes').annotate(
            author_name=F('owner__username')).annotate(likes_count=Count('likes'))
        serializer_data = BlogSerializer(blogs, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_ordering(self):
        url = reverse('blog-list')
        response = self.client.get(url, data={'ordering': '-title'})
        blogs = Blog.objects.all().prefetch_related(
            Prefetch('comments', queryset=Comment.objects.all().annotate(
                owner_name=F('owner__username')))).prefetch_related('likes').annotate(
            author_name=F('owner__username')).annotate(likes_count=Count('likes')).order_by('-title')
        serializer_data = BlogSerializer(blogs, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
