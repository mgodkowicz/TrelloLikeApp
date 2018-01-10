from django.urls import path

from boards.views import BoardsListCreateView, ListsListCreateView, ListDetailView, TasksListCreateView, \
    TaskDetailView, TaskCompletionView, TaskMoveView

urlpatterns = [
    path('', BoardsListCreateView.as_view()),
    path('<int:board_id>/lists', ListsListCreateView.as_view()),
    path('<int:board_id>/lists/<int:list_id>', ListDetailView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks', TasksListCreateView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>', TaskDetailView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/completed', TaskCompletionView.as_view()),
    path('<int:board_id>/lists/<int:list_id>/tasks/<int:task_id>/move/<int:new_list_id>', TaskMoveView.as_view()),
]
