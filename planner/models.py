from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time

User = get_user_model()


class Day(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='days',
        # null=True,
        # blank=True
    )

    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user} - {self.date}"


class HourSlot(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='hours')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('day', 'start_time')
        ordering = ['start_time']

    def label(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    def __str__(self):
        return f"{self.day} {self.label()}"


class Task(models.Model):
    hourslot = models.ForeignKey(HourSlot, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)  # opcional

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} ({self.hourslot})"


class TaskAttachment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.file.name.split('/')[-1]

    def __str__(self):
        return self.filename()


class ChecklistItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='checklists',
        # null=True,
        # blank=True
    )

    URGENCIA_CHOICES = [
        (1, 'Muy Urgente'),
        (2, 'Urgente'),
        (3, 'Normal'),
        (4, 'Baja'),
        (5, 'Informativo')
    ]

    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    urgencia = models.PositiveSmallIntegerField(
        choices=URGENCIA_CHOICES,
        default=3
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class SubChecklistItem(models.Model):
    checklist = models.ForeignKey(
        ChecklistItem,
        related_name='subtasks',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({'✔' if self.completed else '✗'})"
