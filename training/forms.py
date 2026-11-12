from django import forms

from training.models import TrainingSession


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        exclude = ['attendees']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Describe the training session'}
            ),
        }
        labels = {
            'title': 'Session Title',
            'martial_art': 'Martial Art',
            'start_time': 'Start Time',
            'end_time': 'End Time',
        }
        help_texts = {
            'capacity': 'Maximum number of students who can attend.',
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            self.add_error(
                'end_time',
                'End time must be later than start time.'
            )

        return cleaned_data
