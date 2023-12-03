from django.urls import path
from rest_framework.routers import SimpleRouter
import app.viewsets as app_viewsets
import app.views as app_views

router = SimpleRouter()
router.register(r'membership_types', app_viewsets.MembershipTypeViewSet, basename='MembershipType')
router.register(r'users', app_viewsets.UserViewSet, basename='User')
router.register(r'user_memberships', app_viewsets.UserMembershipViewSet, basename='UserMembership')
router.register(r'check_in_check_outs', app_viewsets.CheckInCheckOutViewSet, basename='CheckInCheckOut')

urlpatterns = [
    path('', app_views.main, name='main'),
    path('manage-user-memberships', app_views.manage_user_memberships, name='manage-user-memberships'),
    path('manage-membership', app_views.manage_membership, name='manage-membership'),
    path('user_memberships/<int:pk>/', app_viewsets.UserMembershipViewSet.as_view({'get': 'list'}), name='user-membership-detail')
] + router.get_urls()
