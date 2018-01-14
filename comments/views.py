from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404, get_list_or_404

from boards.models import Task
from comments.models import Comment
from django.contrib.auth.models import User
from comments.serializers import CommentSerializer, CommentCreateSerializer, CommentDetailsSerializer


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentDetailsSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return CommentSerializer
    #     elif self.request.method == 'POST':
    #         return CommentCreateSerializer

    def get_queryset(self):
        return get_list_or_404(Comment, task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        task_obj = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer.save(
            task=task_obj,
            author=self.request.user
        )


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['comment_id'])
