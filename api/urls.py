from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from api import views as api_views
from api import viewsets as api_viewsets

router = SimpleRouter()
router.register(r'Users', api_viewsets.UserViewSet, basename='User')
router.register(r'MembershipTypes', api_viewsets.MembershipTypeViewSet, basename='MembershipType')
router.register(r'MedicalClearances', api_viewsets.MedicalClearanceTypeViewSet, basename='MedicalClearance')

urlpatterns = [
                  # path('getUsers/', api_views.getUsers),
                  # path('getUsers/<int:user_id>', api_views.getUser),
                  # path('addUser/', api_views.addUser),
                  # path('Users/<int:user_id>', api_views.Users),
                  # path('api/Users/<int:pk>/medical_clearance/',
                  #      api_views.UserViewSet.as_view({'get': 'medical_clearance'}),
                  #      name='user-medical-clearance'),
                  path('medical_clearance/<int:user_id>/', api_views.MedicalClearanceDetailView.as_view(),
                       name='medical-clearance-detail'),

              ] + router.get_urls()

urlpatterns = format_suffix_patterns(urlpatterns)
