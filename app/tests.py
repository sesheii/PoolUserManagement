from django.test import TestCase

from django.test import TestCase
from app.models import MembershipType, User, UserMembership, CheckInCheckOut
from datetime import datetime, timedelta

class MembershipTypeModelTest(TestCase):
    def test_string_representation(self):
        membership_type = MembershipType(name="Gold")
        self.assertEqual(str(membership_type), "Gold")

class UserModelTest(TestCase):
    def test_string_representation(self):
        user = User(full_name="John Doe")
        self.assertEqual(str(user), "John Doe")


