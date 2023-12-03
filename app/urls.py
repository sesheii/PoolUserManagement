from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from app.viewsets import MembershipTypeViewSet, UserViewSet, UserMembershipViewSet, CheckInCheckOutViewSet

router = SimpleRouter()
router.register(r'membership_types', MembershipTypeViewSet, basename='MembershipType')
router.register(r'users', UserViewSet, basename='User')
router.register(r'user_memberships', UserMembershipViewSet, basename='UserMembership')
router.register(r'check_in_check_outs', CheckInCheckOutViewSet, basename='CheckInCheckOut')

urlpatterns = [

] + router.get_urls()
