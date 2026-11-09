from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from martial_arts.forms import MartialArtCreateForm, MartialArtEditForm
from martial_arts.models import MartialArt


class MartialArtListView(ListView):
    model = MartialArt


class MartialArtDetailView(DetailView):
    model = MartialArt


class MartialArtCreateView(LoginRequiredMixin, CreateView):
    model = MartialArt
    form_class = MartialArtCreateForm
    success_url = reverse_lazy('martial-art-list')


class MartialArtUpdateView(LoginRequiredMixin, UpdateView):
    model = MartialArt
    form_class = MartialArtEditForm
    success_url = reverse_lazy('martial-art-list')


class MartialArtDeleteView(LoginRequiredMixin, DeleteView):
    model = MartialArt
    success_url = reverse_lazy('martial-art-list')