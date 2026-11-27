from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from training.permissions import IsInstructorOrReadOnly
from training.serializers import TrainingSessionSerializer

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

from training.tasks import generate_attendance_report
from celery import current_app

from django.contrib import messages
from django.conf import settings


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

        context['can_generate_report'] = (
                self.request.user.is_authenticated
                and self.request.user.groups.filter(name='Instructors').exists()
                and self.object.instructor == self.request.user
        )

        if context['can_generate_report']:
            task_id = self.request.session.get(
                f'attendance_report_{self.request.user.pk}_{self.object.pk}'
            )

            if not settings.CELERY_RESULT_BACKEND:
                context['report_status'] = 'UNAVAILABLE'

            elif task_id:
                try:
                    task = current_app.AsyncResult(task_id)
                    context['report_status'] = task.status

                    if context['report_status'] == 'SUCCESS':
                        context['attendance_report'] = task.result

                except Exception:
                    context['report_status'] = 'UNAVAILABLE'

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


class TrainingSessionListCreateAPIView(ListCreateAPIView):
    queryset = TrainingSession.objects.all().order_by('date', 'start_time')
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class TrainingSessionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsInstructorOrReadOnly]


class TrainingSessionReportView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.groups.filter(name='Instructors').exists():
            raise PermissionDenied

        training_session = get_object_or_404(TrainingSession, pk=pk)

        if training_session.instructor != request.user:
            raise PermissionDenied

        if not settings.CELERY_BROKER_URL:
            messages.error(
                request,
                'Attendance report service is unavailable.'
            )
            return redirect('training-detail', pk=pk)

        try:
            task = generate_attendance_report.delay(training_session.pk)

        except Exception:
            messages.error(
                request,
                'Unable to generate attendance report. Please try again later.'
            )
            return redirect('training-detail', pk=pk)

        request.session[f'attendance_report_{request.user.pk}_{pk}'] = task.id

        return redirect('training-detail', pk=pk)