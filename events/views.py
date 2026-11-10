from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from events.forms import EventCreateForm, EventEditForm
from events.models import Event


class EventListView(ListView):
    model = Event
    ordering = 'date'

    def get_queryset(self):
        event_type = self.request.GET.get('type')
        qs = super().get_queryset()

        if event_type:
            qs = qs.filter(event_type=event_type)

        return qs


class EventDetailView(DetailView):
    model = Event


class EventCreateView(PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventCreateForm
    success_url = reverse_lazy('event-list')
    permission_required = 'events.add_event'


class EventUpdateView(PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventEditForm
    success_url = reverse_lazy('event-list')
    permission_required = 'events.change_event'


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('event-list')
    permission_required = 'events.delete_event'
