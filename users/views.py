from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from boards.models import Board, Task
from users.models import UserProjectTeam
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404


class UserCreate(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardAddUserView(APIView):

    def get(self, request, **kwargs):
        board = get_object_or_404(Board, id=self.kwargs['board_id'])
        team = UserProjectTeam.objects.get_or_create(
            id=board.contributors
        )[0]

        user_obj = User.objects.get(id=self.kwargs['user_id'])

        team.user.add(user_obj)
        board.contributors = team
        team.save()
        board.save()

        return Response({
            'board': board.id,
            'user_id': user_obj.id
        })


class AddUserToTask(APIView):

    def get(self, request, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        task.performer_id = user
        task.save()

        return Response({
            'task_id': task.id,
            'user': user.id
        })
