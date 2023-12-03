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
    serializer_class = UserMembershipSerializer

    def get_queryset(self):
        queryset = UserMembership.objects.all()
        user_id = self.kwargs.get('pk', None)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        return queryset


class CheckInCheckOutViewSet(viewsets.ModelViewSet):
    queryset = CheckInCheckOut.objects.all()
    serializer_class = CheckInCheckOutSerializer
