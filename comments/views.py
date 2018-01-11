from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404, get_list_or_404
from comments.models import Comment
from django.contrib.auth.models import User
from comments.serializers import CommentSerializer


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return get_list_or_404(Comment, task_id=self.kwargs['task_id'])


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['comment_id'])
