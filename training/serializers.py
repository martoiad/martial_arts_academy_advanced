from rest_framework import serializers

from training.models import TrainingSession


class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = [
            'id',
            'title',
            'martial_art',
            'instructor',
            'attendees',
            'date',
            'start_time',
            'end_time',
            'capacity',
            'description',
        ]
        read_only_fields = [
            'instructor',
            'attendees',
        ]

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if self.instance:
            start_time = start_time or self.instance.start_time
            end_time = end_time or self.instance.end_time

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                {
                    'end_time': 'End time must be later than start time.'
                }
            )

        return attrs