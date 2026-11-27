from celery import shared_task

from training.models import TrainingSession


@shared_task
def generate_attendance_report(session_id):
    session = TrainingSession.objects.get(pk=session_id)

    return {
        'title': session.title,
        'capacity': session.capacity,
        'registered_students': session.attendees.count(),
        'places_left': session.places_left,
    }