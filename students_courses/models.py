from django.db import models
from django.db.models import UUIDField, TextChoices
from uuid import uuid4


# Create your models here.
class student_course_status(TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"


class StudentCourse(models.Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    status = models.CharField(
        max_length=10,
        choices=student_course_status.choices,
        default=student_course_status.PENDING,
    )
    student = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="students_courses")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="students_courses")
