from django.db.models import Prefetch, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from blogs.models import Blog, Comment, Like
from blogs.serializers import BlogSerializer, LikeSerializer


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all().prefetch_related(Prefetch('comments', queryset=Comment.objects.all().annotate(
        owner_name=F('owner__username')))).prefetch_related('likes').annotate(
        author_name=F('owner__username')).annotate(likes_count=Count('likes'))
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title']
    search_fields = ['title', 'article']
    ordering_fields = ['title', 'date']
    permission_classes = [IsAuthenticatedOrReadOnly]


class LikePostView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'blog'

    def get_object(self):
        obj, created = Like.objects.get_or_create(owner=self.request.user, blog_id=self.kwargs['blog'])
        return obj
