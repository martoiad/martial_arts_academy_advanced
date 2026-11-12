from django.urls import path

from training.views import (
    TrainingSessionCreateView,
    TrainingSessionDeleteView,
    TrainingSessionDetailView,
    TrainingSessionJoinView,
    TrainingSessionLeaveView,
    TrainingSessionListView,
    TrainingSessionUpdateView,
)

urlpatterns = [
    path('', TrainingSessionListView.as_view(), name='training-list'),
    path('create/', TrainingSessionCreateView.as_view(), name='training-create'),
    path('<int:pk>/', TrainingSessionDetailView.as_view(), name='training-detail'),
    path('<int:pk>/edit/', TrainingSessionUpdateView.as_view(), name='training-edit'),
    path('<int:pk>/delete/', TrainingSessionDeleteView.as_view(), name='training-delete'),
    path('<int:pk>/join/', TrainingSessionJoinView.as_view(), name='training-join'),
    path('<int:pk>/leave/', TrainingSessionLeaveView.as_view(), name='training-leave'),
]
