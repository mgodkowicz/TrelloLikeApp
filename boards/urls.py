from django.urls import path

from boards.views import BoardsListCreateView, ListsListCreateView, ListDetailView, TasksListCreateView, \
    TaskDetailView, TaskCompletionView, TaskMoveView
from comments.views import CommentListCreateView, CommentDetailView
from users.views import AddTeamView

app_name = 'boards'

urlpatterns = [
    path(
        '', BoardsListCreateView.as_view(), name='list-create'
    ),
    path(
        '<int:board_id>/add_team/<int:team_id>', # TODO tests
        AddTeamView.as_view(), name='team'
    ),
    path(
        '<int:board_id>/lists',
        ListsListCreateView.as_view(), name="lists-list-create"
    ),
    path(
        '<int:board_id>/lists/<int:list_id>',
        ListDetailView.as_view(), name="list-details"
    ),
    path(
        '<int:board_id>/lists/<int:list_id>/tasks',
        TasksListCreateView.as_view(), name="task-list"
    ),
    path(
        '<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>',
        TaskDetailView.as_view(), name="task-details"
    ),
    # path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/add_user/<int:user_id>', AddUserView.as_view()),
    path(
        '<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/comments',
        CommentListCreateView.as_view(), name='comments-list' # TODO tests
    ),
    path(
        '<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/comments/<int:comment_id>/edit',
        CommentDetailView.as_view()
    ),
    path(
        '<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/completed',
        TaskCompletionView.as_view(), name='task-complete'
    ),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/move/<int:new_list_id>',
         TaskMoveView.as_view(), name='task-move'
         ),
]
