from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from app.models import MembershipType, User, UserMembership, CheckInCheckOut
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from app.views import manage_user_memberships


class MembershipTypeViewSetTest(APITestCase):

    def setUp(self):
        MembershipType.objects.create(name="Basic", description="Basic Membership", duration=30, price=100.00, start_time="00:00:00", end_time="00:00:00")

    def test_get_membership_types(self):
        response = self.client.get('/membership_types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_membership_type(self):
        data = {'name': 'Premium', 'description': 'Premium Membership', 'duration': 60, 'price': 200.00, 'start_time': '00:00:00', 'end_time': '00:00:00'}
        response = self.client.post('/membership_types/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MembershipType.objects.count(), 2)

    def test_update_membership_type(self):
        membership_type = MembershipType.objects.get(name='Basic')
        data = {
            'name': 'Premium Updated',
            'description': 'Updated Premium Membership',
            'duration': 60,
            'price': 10000.00,
            'start_time': '00:00:00',
            'end_time': '00:00:00'
        }
        response = self.client.put(f'/membership_types/{membership_type.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        membership_type.refresh_from_db()
        self.assertEqual(membership_type.name, 'Premium Updated')

    def test_delete_membership_type(self):
        membership_type = MembershipType.objects.get(name='Basic')
        response = self.client.delete(f'/membership_types/{membership_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MembershipType.objects.count(), 0)


class UserViewSetTest(APITestCase):

    def setUp(self):
        # Створення тестових даних
        MembershipType.objects.create(name="Basic", description="Basic Membership", duration=30, price=100.00, start_time="00:00:00", end_time="00:00:00")
        User.objects.create(full_name="Test User", email="testuser@example.com", is_blocked=False)

    def test_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user(self):
        data = {
            'full_name': 'New User',
            'email': 'newuser@example.com',
            'is_blocked': False
        }
        response = self.client.post('/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user(self):
        user = User.objects.get(email='testuser@example.com')
        data = {
            'full_name': 'Updated User',
            'email': 'updateduser@example.com',
            'is_blocked': True
        }
        response = self.client.put(f'/users/{user.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.full_name, 'Updated User')

    def test_delete_user(self):
        user = User.objects.get(email='testuser@example.com')
        response = self.client.delete(f'/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)



class UserMembershipViewSetTest(APITestCase):

    def setUp(self):
        self.membership_type = MembershipType.objects.create(name="Basic", description="Basic Membership", duration=30, price=100.00, start_time="00:00:00", end_time="00:00:00")
        self.user = User.objects.create(full_name="Test User", email="testuser@example.com", is_blocked=False)
        self.start_date = timezone.now().date()
        self.end_date = self.start_date + timedelta(days=30)
        UserMembership.objects.create(user=self.user, membership_type=self.membership_type, start_date=self.start_date, end_date=self.end_date)

    def test_get_user_memberships(self):
        response = self.client.get(f'/user_memberships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_memberships_for_specific_user(self):
        response = self.client.get(f'/user_memberships/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перевірка, що дані відповідають членствам конкретного користувача
        for membership in response.data:
            self.assertEqual(membership['user'], self.user.id)

    def test_create_user_membership(self):
        data = {
            'user': self.user.id,
            'membership_type': self.membership_type.id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date)
        }
        response = self.client.post('/user_memberships/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserMembership.objects.count(), 2)


class CheckInCheckOutViewSetTest(APITestCase):

    def setUp(self):
        # Створення тестових даних
        self.user = User.objects.create(full_name="Test User", email="test@example.com", is_blocked=False)
        self.check_in = CheckInCheckOut.objects.create(
            user=self.user, 
            check_in_time=timezone.now(), 
            check_out_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_get_check_in_check_out_list(self):
        response = self.client.get('/check_in_check_outs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_check_in_check_out(self):
        data = {
            'user': self.user.id,
            'check_in_time': timezone.now(),
            'check_out_time': timezone.now() + timezone.timedelta(hours=2)
        }
        response = self.client.post('/check_in_check_outs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CheckInCheckOut.objects.count(), 2)

    def test_update_check_in_check_out(self):
        new_check_out_time = timezone.now() + timezone.timedelta(hours=3)
        data = {
            'user': self.user.id,
            'check_in_time': self.check_in.check_in_time,
            'check_out_time': new_check_out_time
        }
        response = self.client.put(f'/check_in_check_outs/{self.check_in.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_in.refresh_from_db()
        self.assertEqual(self.check_in.check_out_time, new_check_out_time)

    def test_delete_check_in_check_out(self):
        response = self.client.delete(f'/check_in_check_outs/{self.check_in.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CheckInCheckOut.objects.count(), 0)




class ManageUserMembershipsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(full_name="Test User", email="test@example.com", is_blocked=False)
        self.membership_type = MembershipType.objects.create(name="Basic", description="Basic Membership", duration=30, price=100.00, start_time="00:00", end_time="00:01:00")
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=self.membership_type.duration)
        UserMembership.objects.create(user=self.user, membership_type=self.membership_type, start_date=self.start_date, end_date=self.end_date)

    def add_session_to_request(self, request):
        """ Додавання сесії до тестового запиту """
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def test_get_request(self):
        request = self.factory.get('/manage-user-memberships')
        request.session = {'user_id': self.user.id}
        self.add_session_to_request(request)
        response = manage_user_memberships(request)
        self.assertEqual(response.status_code, 200)

    def test_post_request_assign_membership(self):
        request = self.factory.post('/manage-user-memberships', {
            'assign_membership': 'assign',
            'membership_type': self.membership_type.id
        })
        request.session = {'user_id': self.user.id}
        self.add_session_to_request(request)
        response = manage_user_memberships(request)
        self.assertEqual(response.status_code, 200)
        # Перевірте, чи додано нове членство

    def test_post_request_delete_membership(self):
        user_membership = UserMembership.objects.filter(user=self.user).first()
        request = self.factory.post('/manage-user-memberships', {
            'delete_membership': 'delete',
            'membership_id': user_membership.id
        })
        request.session = {'user_id': self.user.id}
        self.add_session_to_request(request)
        response = manage_user_memberships(request)
        self.assertEqual(response.status_code, 200)
        # Перевірте, чи видалено членство

    # Додайте додаткові тести за необхідності...
