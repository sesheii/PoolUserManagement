from rest_framework import serializers
from app.models import MembershipType, User, UserMembership, CheckInCheckOut


class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMembership
        fields = ['user', 'membership_type', 'start_date', 'end_date']


class CheckInCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInCheckOut
        fields = ['user', 'check_in_time', 'check_out_time']
