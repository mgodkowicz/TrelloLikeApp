from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from boards.models import Board
from users.models import UserProjectTeam
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404


class UserCreate(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddTeamView(APIView):

    def get(self, request, **kwargs):
        board = get_object_or_404(Board, id=self.kwargs['board_id'])
        team = UserProjectTeam.objects.get_or_create(id=self.kwargs['team_id'])[0]
        if board.contributors_id == team.id:
            board.contributors_id = None
            board.save()
            return Response({
                'board': board.id,
                'removed_team': team.id
            })
        else:
            board.contributors_id = team.id
            board.save()
            return Response({
                    'board': board.id,
                    'assigned_team': team.id
                })
