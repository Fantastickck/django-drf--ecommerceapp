from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, SAFE_METHODS, BasePermission


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsAuthorFeedback(BasePermission):
    """
    Permission для авторов отзыва для изменения.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user 
        
