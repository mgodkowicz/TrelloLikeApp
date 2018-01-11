from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from boards.models import Board, List, Task
from boards.serializers import BoardsGetListSerializer, ListsListSerializer, TasksListSerializer
from users.models import UserProjectOwners, UserProjectTeam


class SetUp(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='TestUser')
        self.user2 = User.objects.create(username='TestUser2')
        self.owner = UserProjectOwners.objects.create(
            user=self.user
        )
        another_owner = UserProjectOwners.objects.create(
            user=self.user
        )
        self.client.force_authenticate(self.user)

        self.board = Board.objects.create(
            owner_id=self.owner,
            name='My first board'
        )

        Board.objects.create(
            owner_id=another_owner,
            name='Not user board'
        )

        self.list_obj = List.objects.create(
            name="TODO",
            board_id=self.board
        )

        self.task_obj = Task.objects.create(
            name="Data aggregation",
            list_id=self.list_obj,
            priority=4,
            description="Do this and this",
            deadline=datetime(2018, 1, 1),
            performer_id=self.user
        )


class GetAllUserBoardsTest(SetUp):

    def test_get_all_user_boards(self):
        response = self.client.get(reverse(
            'boards:list-create'
        ))
        boards = Board.objects.filter(owner_id=self.owner)
        serializer = BoardsGetListSerializer(boards, many=True)
        self.assertEqual(len(boards), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_logged_user_get_all_boards(self):
        self.client.logout()
        response = self.client.get(reverse('boards:list-create'))
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)


class BoardCreateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='TestUser')
        self.client.force_authenticate(user=user)

        self.valid_payload = {
            'name': 'Great Project'
        }
        self.invalid_payload = {}

    def test_create_valid_board(self):
        response = self.client.post(
            reverse('boards:list-create'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_board(self):
        response = self.client.post(
            reverse('boards:list-create'),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_board_unauthorized(self):
        self.client.logout()
        response = self.client.post(
            reverse('boards:list-create'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAllBoardListsTest(SetUp):

    def test_get_all_board_list(self):
        response = self.client.get(
            reverse('boards:lists-list-create', kwargs={'board_id': 1})
        )
        lists = List.objects.filter(board_id=self.board)
        serializer = ListsListSerializer(lists, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_logged_user_get_all_boards(self):
        self.client.logout()
        response = self.client.get(
            reverse('boards:lists-list-create', kwargs={'board_id': 1})
        )
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)

    def test_get_list_for_invalid_board(self):
        response = self.client.get(
            reverse('boards:lists-list-create', kwargs={'board_id': 10})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ListsCreateTest(SetUp):
    def setUp(self):
        super(ListsCreateTest, self).setUp()

        self.valid_payload = {
            'name': 'Great Project'
        }
        self.invalid_payload = {}

    def test_create_valid_list(self):
        response = self.client.post(
            reverse('boards:lists-list-create', kwargs={'board_id': 1}),
            data=self.valid_payload
        )
        list_obj = List.objects.all().first()
        self.assertEqual(list_obj.board_id.id, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_list(self):
        response = self.client.post(
            reverse('boards:lists-list-create', kwargs={'board_id': 1}),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_list_invalid_url(self):
        response = self.client.post(
            reverse('boards:lists-list-create', kwargs={'board_id': 10}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_list_unauthorized(self):
        self.client.logout()
        response = self.client.post(
            reverse('boards:lists-list-create', kwargs={'board_id': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleListTest(SetUp):

    def test_get_valid_single_list(self):
        response = self.client.get(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    )
        )
        list_odb = List.objects.first()
        serializer = ListsListSerializer(list_odb)
        self.assertEqual(list_odb.id, self.list_obj.id)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_list_invalid_board(self):
        response = self.client.get(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': 1000
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_single_list(self):
        response = self.client.get(
            reverse('boards:list-details',
                    kwargs={'board_id': 100,
                            'list_id': self.list_obj.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleListTest(SetUp):

    def setUp(self):
        super(UpdateSingleListTest, self).setUp()
        self.valid_payload = {
            'name': 'Great Project'
        }
        self.invalid_payload = {}

    def test_valid_update_list(self):
        response = self.client.put(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    ), data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_list(self):
        response = self.client.put(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    ), data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleListTest(SetUp):
    def test_valid_delete_place(self):
        response = self.client.delete(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_place(self):
        response = self.client.delete(
            reverse('boards:list-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': 100
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetListTasksTest(SetUp):

    def test_get_all_list_tasks(self):
        response = self.client.get(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    )
        )
        tasks = Task.objects.filter(list_id=self.list_obj)
        serializer = TasksListSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_logged_user_get_all_tasks(self):
        self.client.logout()
        response = self.client.get(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    )
        )
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)

    def test_get_tasks_for_invalid_list(self):
        response = self.client.get(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': 100
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskCreateTest(SetUp):
    def setUp(self):
        super(TaskCreateTest, self).setUp()

        self.valid_payload = {
            'name': 'write unitests',
            'description': "Test every line of code",
            'priority': 5,
            'deadline': datetime(2018, 4, 1)
        }
        self.invalid_payload = {
            'priority': 5,
            'description': "Test every line of code",
        }

    def test_create_valid_task(self):
        response = self.client.post(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    ),
            data=self.valid_payload
        )
        task_obj = Task.objects.first()
        self.assertEqual(task_obj.list_id.id, self.board.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_list(self):
        response = self.client.post(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    ),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_list_invalid_url(self):
        response = self.client.post(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': 1000
                            }
                    ),
            data=self.valid_payload

        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_list_unauthorized(self):
        self.client.logout()
        response = self.client.post(
            reverse('boards:task-list',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id
                            }
                    ),
            data=self.valid_payload

        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleTaskTest(SetUp):

    def test_get_valid_single_task(self):
        response = self.client.get(
            reverse('boards:task-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': self.list_obj.id,
                            'task_id': self.task_obj.id
                            }
                    )
        )
        task_obj = Task.objects.first()
        serializer = TasksListSerializer(task_obj)
        self.assertEqual(task_obj.id, self.task_obj.id)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_task_invalid_board(self):
        response = self.client.get(
            reverse('boards:task-details',
                    kwargs={'board_id': self.board.id,
                            'list_id': 1000,
                            'task_id': self.task_obj.id
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_single_task(self):
        response = self.client.get(
            reverse('boards:task-details',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': 100
                            }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskManagementTest(SetUp):
    def setUp(self):
        super(TaskManagementTest, self).setUp()

    def test_set_task_as_completed(self):
        task_status = self.task_obj.finished
        response = self.client.get(
            reverse('boards:task-complete',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': self.task_obj.id
                        }
                    )
        )
        expected = {
            'task_id': self.task_obj.id,
            'finished': not task_status
        }

        task = Task.objects.get(id=self.task_obj.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
        self.assertEqual(task.finished, not task_status)

    def test_move_task(self):
        new_list = List.objects.create(
            name="Done",
            board_id=self.board
        )

        response = self.client.get(
            reverse('boards:task-move',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': self.task_obj.id,
                        'new_list_id': new_list.id
                        }
                    )
        )
        expected = {
            'task_id': self.task_obj.id,
            'new_list_id': new_list.id
        }
        task = Task.objects.get(id=self.task_obj.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
        self.assertEqual(task.list_id.id, new_list.id)

    def test_move_task_to_invalid_list(self):
        response = self.client.get(
            reverse('boards:task-move',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': self.task_obj.id,
                        'new_list_id': 20
                    }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_invalid_task_as_completed(self):
        response = self.client.get(
            reverse('boards:task-complete',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': 20
                        }
                    )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_add_user_to_task(self):
        old_performer = self.task_obj.performer_id
        response = self.client.get(
            reverse('boards:task-add-user',
                    kwargs={
                        'board_id': self.board.id,
                        'list_id': self.list_obj.id,
                        'task_id': self.task_obj.id,
                        'user_id': self.user2.id
                        }
                    )
        )
        self.task_obj.refresh_from_db()
        self.assertEqual(self.task_obj.performer_id.id, self.user2.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_performer, self.task_obj.performer_id)


class BoardAddUserTest(SetUp):
    def setUp(self):
        super(BoardAddUserTest, self).setUp()

    def test_add_user(self):
        response = self.client.get(
            reverse('boards:add-user',
                    kwargs={
                        'board_id': self.board.id,
                        'user_id': self.user2.id
                    })
        )
        board = Board.objects.get(id=self.board.id)
        team = UserProjectTeam.objects.filter(
            id=board.contributors.id
        ).first()

        self.assertEqual(board.contributors, team)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
