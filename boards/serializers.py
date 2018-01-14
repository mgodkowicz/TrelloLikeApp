from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from boards.models import Board, List, Task
from comments.serializers import CommentSerializer, CommentDetailsSerializer
from users.models import UserProjectTeam
from users.serializers import UserDetailsSerializer


class BoardsGetListSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardsPostListSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['name']


class TasksListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ListsListSerializer(ModelSerializer):
    tasks = TasksListSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'tasks']


class TasksPostListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'deadline']


class TaskDetailsSerializer(ModelSerializer):
    comments = CommentDetailsSerializer(many=True, read_only=True)
    performer_id = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class ListTeamSerializer(ModelSerializer):

    user = UserDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = UserProjectTeam
        fields = '__all__'
