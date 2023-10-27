from django.urls import path
from . import views

urlpatterns = [
    path("courses/<course_id>/contents/", views.ContentCourseView.as_view()),
    path("courses/<uuid:course_id>/contents/<uuid:content_id>/", views.ContentDetailView.as_view()),
]
