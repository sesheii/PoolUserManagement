from django.contrib import admin
from app.models import MembershipType, User, UserMembership, CheckInCheckOut


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration', 'price')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_blocked')
    filter_horizontal = ('memberships',)


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'start_date', 'end_date')


@admin.register(CheckInCheckOut)
class CheckInCheckOutAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_in_time', 'check_out_time')
