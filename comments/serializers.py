from rest_framework.serializers import ModelSerializer

from users.serializers import UserDetailsSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentDetailsSerializer(ModelSerializer):
    author = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created', 'author']


class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']
