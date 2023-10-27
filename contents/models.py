from django.db import models
from django.db.models import UUIDField
from uuid import uuid4


# Create your models here.
class Content(models.Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=150)
    content = models.TextField()
    video_url = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="contents"
    )
