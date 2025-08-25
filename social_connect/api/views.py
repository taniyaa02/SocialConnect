from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Profile
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer
from django.contrib.auth.models import User
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        profile_to_follow = self.get_object()
        user = request.user
        if profile_to_follow.user in user.profile.following.all():
            user.profile.following.remove(profile_to_follow.user)
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        else:
            user.profile.following.add(profile_to_follow.user)
            return Response({'status': 'followed'}, status=status.HTTP_200_OK)