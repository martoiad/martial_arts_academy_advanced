from django.urls import path

from training.views import (
    TrainingSessionCreateView,
    TrainingSessionDetailView,
    TrainingSessionListView,
)

urlpatterns = [
    path('', TrainingSessionListView.as_view(), name='training-list'),
    path('create/', TrainingSessionCreateView.as_view(), name='training-create'),
    path('<int:pk>/', TrainingSessionDetailView.as_view(), name='training-detail'),
]
