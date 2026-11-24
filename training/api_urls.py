from django.urls import path

from training.views import (
    TrainingSessionDetailAPIView,
    TrainingSessionListCreateAPIView,
)


urlpatterns = [
    path(
        '',
        TrainingSessionListCreateAPIView.as_view(),
        name='api-training-list-create',
    ),
    path(
        '<int:pk>/',
        TrainingSessionDetailAPIView.as_view(),
        name='api-training-detail',
    ),
]