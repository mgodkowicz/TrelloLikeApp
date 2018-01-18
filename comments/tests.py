from rest_framework import status
from boards.tests import SetUp
from django.urls import reverse

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentDetailsSerializer


class GetCommentsListTests(SetUp):
    def setUp(self):
        super(GetCommentsListTests, self).setUp()

        self.comment_obj1 = Comment.objects.create(
            content='foo content',
            author=self.user,
            task=self.task_obj
        )
        self.comment_obj2 = Comment.objects.create(
            content='foo content2',
            author=self.user,
            task=self.task_obj
        )

    def test_should_get_all_task_comments(self):
        response = self.client.get(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                             'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    )
        )
        comments = Comment.objects.filter(task_id=self.task_obj.id)
        serializer = CommentDetailsSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_get_all_comments_for_not_logged_user(self):
        self.client.logout()
        response = self.client.get(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    )
        )
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)

    def test_should_not_get_comments_list_for_invalid_task(self):
        response = self.client.get(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id':  0
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentsCreateTest(SetUp):
    def setUp(self):
        super(CommentsCreateTest, self).setUp()

        self.valid_payload = {
            'content': 'write content',
            'author': self.user.id,
            'task': self.task_obj.id
        }
        self.invalid_payload = {}

    def test_should_create_valid_comment(self):
        response = self.client.post(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    ),
            data=self.valid_payload
        )
        comment_obj = Comment.objects.all().first()
        self.assertEqual(comment_obj.author_id, self.user.id)
        self.assertEqual(comment_obj.task_id, self.task_obj.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_not_create_invalid_comment(self):
        response = self.client.post(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    ),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_unauthorized_comment(self):
        self.client.logout()
        response = self.client.post(
            reverse('boards:comments-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    ),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleCommentTest(SetUp):
    def setUp(self):
        super(GetSingleCommentTest, self).setUp()

        self.comment_obj1 = Comment.objects.create(
            content='foo content',
            author=self.user,
            task=self.task_obj
        )

    def test_should_get_single_comment(self):
        response = self.client.get(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_get_single_comment_for_invalid_comment_id(self):
        response = self.client.get(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': 200
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_get_single_comment_for_unauthorised(self):
        self.client.logout()
        response = self.client.get(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateSingleCommentTest(SetUp):
    def setUp(self):
        super(UpdateSingleCommentTest, self).setUp()

        self.comment_obj1 = Comment.objects.create(
            content='foo content',
            author=self.user,
            task=self.task_obj
        )
        self.valid_payload = {
            'content': 'No can do',
            'author': self.user.id,
            'task': self.task_obj.id
        }
        self.invalid_payload = {}

    def test_should_update_valid_comment(self):
        response = self.client.put(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    ),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_update_invalid_comment(self):
        response = self.client.put(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    ),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCommentTest(SetUp):
    def setUp(self):
        super(DeleteSingleCommentTest, self).setUp()

        self.comment_obj1 = Comment.objects.create(
            content='foo content',
            author=self.user,
            task=self.task_obj
        )

    def test_valid_delete_place(self):
        response = self.client.delete(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_place(self):
        response = self.client.delete(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': 10000
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorised_delete_place(self):
        self.client.logout()
        response = self.client.delete(
            reverse('boards:comment-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id,
                            'comment_id': self.comment_obj1.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
