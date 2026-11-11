from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from training.forms import TrainingSessionForm
from training.models import TrainingSession


class TrainingSessionListView(ListView):
    model = TrainingSession
    ordering = ['date', 'start_time']


class TrainingSessionDetailView(DetailView):
    model = TrainingSession


class TrainingSessionCreateView(PermissionRequiredMixin, CreateView):
    model = TrainingSession
    form_class = TrainingSessionForm
    success_url = reverse_lazy('training-list')
    permission_required = 'training.add_trainingsession'
