from contents.models import Content
from rest_framework.permissions import BasePermission


class IsAdminCanAccessContent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        course_id = view.kwargs["course_id"]
        content_id = view.kwargs["content_id"]
        content = Content.objects.get(id=content_id)

        if content.course.students.filter(id=request.user.id).exists():
            return True

        return False
