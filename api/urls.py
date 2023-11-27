from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from api import views as api_views
from api import viewsets as api_viewsets


router = SimpleRouter()
router.register(r'Users', api_viewsets.UserViewSet, basename='User')
router.register(r'MembershipTypes', api_viewsets.MembershipTypeViewSet, basename='MembershipType')

urlpatterns = [
    # path('getUsers/', api_views.getUsers),
    # path('getUsers/<int:user_id>', api_views.getUser),
    # path('addUser/', api_views.addUser),
    # path('UsersGay/', api_views.CreateUsers),
    # path('Users/<int:user_id>', api_views.Users),

] + router.get_urls()

urlpatterns = format_suffix_patterns(urlpatterns)
