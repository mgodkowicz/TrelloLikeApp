from rest_framework.serializers import ModelSerializer

from boards.models import Board, List, Task


class BoardsListSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class ListsListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name']


class TasksListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'