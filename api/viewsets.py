from rest_framework import viewsets

from api.models import User, MembershipType, MedicalClearance
from api.serializers import UserSerializer, MembershipTypeSerializer, MedicalClearanceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MembershipTypeViewSet(viewsets.ModelViewSet):
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer


class MedicalClearanceTypeViewSet(viewsets.ModelViewSet):
    queryset = MedicalClearance.objects.all()
    serializer_class = MedicalClearanceSerializer
