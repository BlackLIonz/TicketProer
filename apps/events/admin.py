from django.contrib import admin
from django.http import HttpResponseRedirect

from apps.events.models import Event


class EventAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    change_form_template = 'admin/events/event/change_form.html'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        if '_make-approve' in request.POST:
            obj.is_approved = True
            obj.save()
            return HttpResponseRedirect('.')
        elif '_make-reject'in request.POST:
            obj.is_approved = False
            obj.save()
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)


admin.site.register(Event, EventAdmin)
