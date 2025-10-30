from rest_framework import permissions

class IsSellerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print('role:',request.user.groups.filter(name="Seller").exists())
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user and 
            user.is_authenticated and (
                request.user.groups.filter(name="Seller").exists() or user.is_staff
            )
        )
    