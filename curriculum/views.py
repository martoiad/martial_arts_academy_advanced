from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)

from curriculum.forms import CurriculumItemCreateForm
from curriculum.models import CurriculumItem


class CurriculumItemListView(ListView):
    model = CurriculumItem
    ordering = ['martial_art', 'level', 'name']


class CurriculumItemDetailView(DetailView):
    model = CurriculumItem


class CurriculumItemCreateView(PermissionRequiredMixin, CreateView):
    model = CurriculumItem
    form_class = CurriculumItemCreateForm
    success_url = reverse_lazy('curriculum-list')
    permission_required = 'curriculum.add_curriculumitem'
