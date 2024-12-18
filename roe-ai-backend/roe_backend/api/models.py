from django.db import models

class Video(models.Model):
    file = models.FileField()
    transcription = models.TextField(null=True, blank=True)
    transcription_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)  # Added field

    def __str__(self):
        return f"Video: {self.title or 'Untitled'}"