from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from training.forms import TrainingSessionForm
from training.models import TrainingSession

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import View


class TrainingSessionListView(ListView):
    model = TrainingSession
    ordering = ['date', 'start_time']


class TrainingSessionDetailView(DetailView):
    model = TrainingSession

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_student'] = (
                self.request.user.is_authenticated
                and self.request.user.groups.filter(name='Students').exists()
        )

        return context


class TrainingSessionCreateView(PermissionRequiredMixin, CreateView):
    model = TrainingSession
    form_class = TrainingSessionForm
    success_url = reverse_lazy('training-list')
    permission_required = 'training.add_trainingsession'


class TrainingSessionUpdateView(PermissionRequiredMixin, UpdateView):
    model = TrainingSession
    form_class = TrainingSessionForm
    success_url = reverse_lazy('training-list')
    permission_required = 'training.change_trainingsession'


class TrainingSessionDeleteView(PermissionRequiredMixin, DeleteView):
    model = TrainingSession
    success_url = reverse_lazy('training-list')
    permission_required = 'training.delete_trainingsession'


class TrainingSessionJoinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.groups.filter(name='Students').exists():
            raise PermissionDenied

        training_session = get_object_or_404(TrainingSession, pk=pk)

        if (
                request.user not in training_session.attendees.all()
                and not training_session.is_full
        ):
            training_session.attendees.add(request.user)

        return redirect('training-detail', pk=pk)


class TrainingSessionLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.groups.filter(name='Students').exists():
            raise PermissionDenied

        training_session = get_object_or_404(TrainingSession, pk=pk)

        training_session.attendees.remove(request.user)

        return redirect('training-detail', pk=pk)
