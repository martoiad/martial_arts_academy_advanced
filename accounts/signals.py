from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_new_user_to_students_group(sender, instance, created, **kwargs):
    if created:
        students_group = Group.objects.filter(name='Students').first()

        if students_group:
            instance.groups.add(students_group)