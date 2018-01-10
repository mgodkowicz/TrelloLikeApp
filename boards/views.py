from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from boards.models import Board, List, Task
from users.models import UserProjectOwners
from boards.serializers import BoardsGetListSerializer, ListsListSerializer, TasksListSerializer, \
    BoardsPostListSerializer, TasksPostListSerializer


class BoardsListCreateView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardsGetListSerializer
        elif self.request.method == 'POST':
            return BoardsPostListSerializer

    def get_queryset(self):
        user = get_object_or_404(UserProjectOwners, id=self.request.user.id)
        return Board.objects.filter(owner_id=user)

    def perform_create(self, serializer):
        new_owner = UserProjectOwners.objects.get_or_create(user=self.request.user)[0]
        serializer.save(
            owner_id=new_owner
        )


class ListsListCreateView(ListCreateAPIView):
    serializer_class = ListsListSerializer

    def get_queryset(self):
        board = get_object_or_404(Board, id=self.kwargs['board_id'])
        return List.objects.filter(board_id=board)

    def perform_create(self, serializer):
        board = get_object_or_404(Board, id=self.kwargs['board_id'])
        serializer.save(
            board_id=board
        )


class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListsListSerializer
    queryset = List.objects.all()

    def get_object(self):
        return get_object_or_404(List, board_id=self.kwargs['board_id'], id=self.kwargs['list_id'])
        #return self.queryset.get(board_id=self.kwargs['board_id'], id=self.kwargs['list_id'])


class TasksListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TasksListSerializer
        elif self.request.method == 'POST':
            return TasksPostListSerializer

    def perform_create(self, serializer):
        list_obj = get_object_or_404(List, id=self.kwargs['list_id'])
        serializer.save(
            list_id=list_obj
        )

    def get_queryset(self):
        list_obj = get_object_or_404(List, id=self.kwargs['list_id'])
        return Task.objects.filter(list_id=list_obj)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TasksListSerializer
    queryset = Task.objects.all()

    def get_object(self):
        return get_object_or_404(Task, id=self.kwargs['task_id'], list_id=self.kwargs['list_id'])


class TaskCompletionView(APIView):

    def get(self, request, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])
        task.finished = not task.finished
        task.save()
        return Response({
            'task_id': task.id,
            'finished': task.finished
        })


class TaskMoveView(APIView):

    def get(self, request, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])
        task.list_id = get_object_or_404(List, id=kwargs['new_list_id'])
        task.save()
        return Response(
            {
                'task_id': task.id,
                'new_list_id': task.list_id.id
            })
