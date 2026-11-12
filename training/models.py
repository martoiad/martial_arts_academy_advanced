from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

from martial_arts.models import MartialArt


class TrainingSession(models.Model):
    title = models.CharField(max_length=100)
    martial_art = models.ForeignKey(
        MartialArt,
        on_delete=models.CASCADE,
        related_name='training_sessions',
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='instructed_sessions',
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='attended_training_sessions',
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def places_left(self):
        return self.capacity - self.attendees.count()

    @property
    def is_full(self):
        return self.attendees.count() >= self.capacity
