from rest_framework import serializers
from api.models import User, MembershipType, MedicalClearance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'


class MedicalClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalClearance
        fields = '__all__'
