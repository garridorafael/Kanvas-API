from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from courses.models import Course
from students_courses.models import StudentCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]
        extra_kwargs = {
            "name": {
                "validators": [
                    UniqueValidator(
                        queryset=Course.objects.all(),
                        message="course with this name already exists.",
                    )
                ]
            },
            "instructor": {"required": False},
            "contents": {"required": False},
            "students_courses": {"required": False},
        }

        def create(self, validated_data: dict) -> Course:
            return Course.objects.create_user(**validated_data)


class StudentCourseSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    student_email = serializers.EmailField(source="student.email", read_only=True)

    class Meta:
        model = StudentCourse
        fields = ["id", "student_id", "student_username", "student_email", "status"]


class CourseStudentSerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"]
