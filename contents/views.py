from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from contents.models import Content
from contents.permissions import IsAdminCanAccessContent
from contents.serializer import ContentSerializer
from courses.models import Course
from courses.permissions import IsAdminOrReadOnly


# Create your views here.
class ContentCourseView(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "course_id"

    def perform_create(self, serializer):
        course_id = self.kwargs.get(self.lookup_url_kwarg)
        serializer.save(course_id=course_id)


class ContentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminCanAccessContent]
    lookup_url_kwarg = "content_id"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Content.objects.all()
        elif user.is_authenticated:
            return Course.objects.filter(students=user)

    def retrieve(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        content_id = kwargs.get("content_id")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "course not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response(
                {"detail": "content not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(content)
        return Response(serializer.data)
