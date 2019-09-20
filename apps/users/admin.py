from django.contrib import admin

from apps.users.models import User, Organization, MembersList


class MembershipInLine(admin.StackedInline):
    model = MembersList


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [MembershipInLine]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [MembershipInLine]


admin.site.register(MembersList)
