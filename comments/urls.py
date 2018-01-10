from django.urls import path
from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path('<int:task_id>/', CommentListCreateView.as_view()),
    path('<int:task_id>/edit', CommentDetailView.as_view())
]