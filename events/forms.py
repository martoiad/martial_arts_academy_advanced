from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from events.models import Event


class EventBaseForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        labels = {
            'title': 'Event Title',
            'event_type': 'Event Type',
            'description': 'Description',
            'date': 'Event Date',
            'location': 'Location',
            'guest_name': 'Special Guest',
            'martial_arts': 'Martial Arts',
        }

        help_texts = {
            'martial_arts': 'Select all martial arts participating in the event.',
        }

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter event title',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe the event',
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Enter event location',
                }
            ),
            'guest_name': forms.TextInput(
                attrs={
                    'placeholder': 'Optional special guest',
                }
            ),
            'martial_arts': forms.CheckboxSelectMultiple(),
        }


class EventCreateForm(EventBaseForm):
    def clean_date(self):
        event_date = self.cleaned_data.get('date')

        if event_date < date.today():
            raise ValidationError(
                'Event date cannot be in the past.'
            )

        return event_date


class EventEditForm(EventBaseForm):
    ...