from rest_framework.permissions import BasePermission

from apps.events.models import Event


class IsOwnerOrAdmin(BasePermission):
    """Access have only author and staff"""
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.created_by.id)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.created_by.id)


class IsSubscriberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.user.id)


class IsVisited(BasePermission):
    """Access have only who visited event"""
    def has_object_permission(self, request, view, obj):
        events = [sub.event for sub in request.user.all_active_subscriptions if sub.event.status == Event.SUCCEED]
        return bool(obj in events)

