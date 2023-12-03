from rest_framework import viewsets
from app.models import MembershipType, User, UserMembership, CheckInCheckOut
from app.serializers import MembershipTypeSerializer, UserSerializer, UserMembershipSerializer, \
    CheckInCheckOutSerializer


class MembershipTypeViewSet(viewsets.ModelViewSet):
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMembershipViewSet(viewsets.ModelViewSet):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer


class CheckInCheckOutViewSet(viewsets.ModelViewSet):
    queryset = CheckInCheckOut.objects.all()
    serializer_class = CheckInCheckOutSerializer
