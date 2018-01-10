from rest_framework.serializers import ModelSerializer

from boards.models import Board, List, Task


class BoardsGetListSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardsPostListSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['name']


class ListsListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name']


class TasksListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TasksPostListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'deadline']
