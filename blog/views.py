from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, 
    PostDetailSerializer, 
    CommentSerializer, 
    LikeSerializer
)
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        
        # Check if the user already liked the post
        like, created = Like.objects.get_or_create(post=post, user=user)
        
        if created:
            return Response({'detail': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, slug=None):
        post = self.get_object()
        user = request.user
        
        # Check if the user already liked the post
        like = Like.objects.filter(post=post, user=user).first()
        
        if like:
            like.delete()
            return Response({'detail': 'Post unliked successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, slug=None):
        post = self.get_object()
        serializer = CommentSerializer(data={'post': post.id, 'content': request.data.get('content')}, 
                                      context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        if 'post_slug' in self.kwargs:
            return Comment.objects.filter(post__slug=self.kwargs['post_slug'])
        return super().get_queryset()

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head']  # Only allow these methods
    
    def get_queryset(self):
        if 'post_slug' in self.kwargs:
            return Like.objects.filter(post__slug=self.kwargs['post_slug'])
        return super().get_queryset()
