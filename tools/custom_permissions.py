from rest_framework.permissions import BasePermission

from apps.events.models import Event


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.created_by.id)


class IsVisited(BasePermission):
    def has_object_permission(self, request, view, obj):
        events = [sub.event for sub in request.user.all_active_subscriptions if sub.event.status == Event.SUCCEED]
        return bool(obj in events)
