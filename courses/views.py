from django.http import Http404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.models import Account
from contents.models import Content
from contents.serializer import ContentSerializer
from courses.models import Course
from courses.permissions import IsAdminOrReadOnly, IsAdminOrStudentCanAccessContent
from courses.serializers import CourseSerializer, CourseStudentSerializer


# Create your views here.
class CourseView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if "instructor" in serializer.validated_data:
            serializer.save(instructor=serializer.validated_data["instructor"])
        else:
            serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Course.objects.all()
        elif user.is_authenticated:
            return Course.objects.filter(students=user)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "course_id"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Course.objects.all()
        elif user.is_authenticated:
            return Course.objects.filter(students=user)


class CourseStudentView(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseStudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "course_id"

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        student_emails = request.data.get("students_courses", [])

        students = []
        non_existent_students = []

        for data in student_emails:
            email = data.get("student_email")
            student = Account.objects.filter(email=email).first()
            if student:
                students.append(student)
            else:
                non_existent_students.append(email)

        if non_existent_students:
            return Response(
                {
                    "detail": f"No active accounts was found: {', '.join(non_existent_students)}."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        course.students.add(*students)

        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


