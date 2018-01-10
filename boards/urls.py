from django.urls import path

from boards.views import BoardsListCreateView, ListsListCreateView, ListDetailView, TasksListCreateView, \
    TaskDetailView, TaskCompletionView, TaskMoveView
from comments.views import CommentListCreateView, CommentDetailView
from users.views import AddTeamView

urlpatterns = [
    path('', BoardsListCreateView.as_view()),
    path('<int:board_id>/add_team/<int:team_id>', AddTeamView.as_view()),
    path('<int:board_id>/lists', ListsListCreateView.as_view()),
    path('<int:board_id>/lists/<int:list_id>', ListDetailView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks', TasksListCreateView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>', TaskDetailView.as_view()),
    # path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/add_user/<int:user_id>', AddUserView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/comments', CommentListCreateView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/comments/<int:comment_id>/edit', CommentDetailView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/completed', TaskCompletionView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/move/<int:new_list_id>', TaskMoveView.as_view()),
]
