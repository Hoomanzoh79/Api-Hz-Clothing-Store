from rest_framework.permissions import IsAuthenticated

class IsNotAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)