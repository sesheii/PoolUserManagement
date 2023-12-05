from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
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


class ManageMembershipsTest(TestCase):
    def setUp(self):
        self.membership_type = MembershipType.objects.create(
            name="Test Membership", 
            description="A test membership", 
            duration=30, 
            price=50.00, 
            start_time=timezone.now(), 
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_add_membership(self):
        url = reverse('manage-memberships')
        data = {
            'name': 'New Membership',
            'description': 'New membership description',
            'duration': 15,
            'price': 100.00,
            'start_time': timezone.now().time(),
            'end_time': (timezone.now() + timezone.timedelta(hours=1)).time(),
        }
        self.client.post(url, data)
        self.assertTrue(MembershipType.objects.filter(name='New Membership').exists())

    def test_delete_membership(self):
        url = reverse('manage-memberships')
        self.client.post(url, {'delete_membership_id': self.membership_type.id})
        self.assertFalse(MembershipType.objects.filter(id=self.membership_type.id).exists())


class CheckInCheckOutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(full_name="Test User", email="test@example.com", is_blocked=False)
        self.membership_type = MembershipType.objects.create(
            name="Standard Membership",
            description="Standard Plan",
            duration=30,
            price=100.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )
        UserMembership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=self.membership_type.duration)
        )


    def test_check_in_user(self):
        url = reverse('check-in-check-out')
        self.client.post(url, {'user_id': self.user.id, 'check_in': 'check_in'})
        self.assertTrue(CheckInCheckOut.objects.filter(user=self.user).exists())
        session = CheckInCheckOut.objects.get(user=self.user)
        self.assertIsNone(session.check_out_time)

    def test_check_out_user(self):
        session = CheckInCheckOut.objects.create(user=self.user, check_in_time=timezone.now())
        url = reverse('check-in-check-out')
        self.client.post(url, {'user_id': self.user.id, 'check_out_session': 'check_out', 'session_id': session.id})
        session.refresh_from_db()
        self.assertIsNotNone(session.check_out_time)


    def test_display_sessions(self):
        CheckInCheckOut.objects.create(user=self.user, check_in_time=timezone.now())
        url = reverse('check-in-check-out')
        response = self.client.post(url, {'user_id': self.user.id})

        self.assertIn('all_sessions', response.context)
        self.assertEqual(len(response.context['all_sessions']), 1)


class RegisterUserTest(TestCase):
    def test_register_user(self):
        url = reverse('register-user')
        user_data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'is_blocked': False,
        }
        response = self.client.post(url, user_data)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())
        new_user = User.objects.get(email='testuser@example.com')
        self.assertEqual(self.client.session['user_id'], new_user.id)
        self.assertRedirects(response, reverse('manage-user-memberships'))


class ViewUsersTest(TestCase):
    def setUp(self):
        User.objects.create(
            full_name="John Doe", 
            email="john@example.com",
            is_blocked=False
        )
        User.objects.create(
            full_name="sshi user", 
            email="sshi@example.com",
            is_blocked=False
        )

    def test_search_users(self):
        url = reverse('view-users')

        response = self.client.get(url, {'query': 'John'})
        users_in_response = response.context['users']
        self.assertEqual(users_in_response.count(), 1)
        self.assertEqual(users_in_response.first().full_name, "John Doe")

        response = self.client.get(url, {'query': 'hn@e'})
        users_in_response = response.context['users']
        self.assertEqual(users_in_response.count(), 1)
        self.assertEqual(users_in_response.first().full_name, "John Doe")

        response = self.client.get(url, {'query': 'sshi@example.com'})
        users_in_response = response.context['users']
        self.assertEqual(users_in_response.count(), 1)
        self.assertEqual(users_in_response.first().full_name, "sshi user")

        response = self.client.get(url, {'query': 'ghost'})
        users_in_response = response.context['users']
        self.assertEqual(users_in_response.count(), 0)


class ManageUserMembershipsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            full_name="Test User", 
            email="test@example.com", 
            is_blocked=False
        )
        self.membership_type = MembershipType.objects.create(
            name="Basic", 
            description="Basic Membership", 
            duration=30, 
            price=100.00, 
            start_time=timezone.now(), 
            end_time=timezone.now() + timedelta(minutes=1)
        )
        self.client.session['user_id'] = self.user.id
        self.client.session.save()

    def test_user_data_not_empty(self):
        url = reverse('manage-user-memberships')
        response = self.client.post(url, {'user_id': self.user.id, 'submit_button': 'submit'})
        self.assertIsNotNone(response.context.get('user_data'))
        self.assertEqual(response.context.get('user_data').id, self.user.id)

    def test_delete_user_membership(self):
        user_membership = UserMembership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )

        url = reverse('manage-user-memberships')
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        self.client.post(url, {
            'delete_membership': 'delete',
            'membership_id': user_membership.id
        })

        self.assertFalse(UserMembership.objects.filter(id=user_membership.id).exists())
        self.assertFalse(UserMembership.objects.filter(id=user_membership.id).exists())

    def test_add_user_membership(self):
        url = reverse('manage-user-memberships')
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        self.client.post(url, {
            'assign_membership': 'assign',
            'membership_type': self.membership_type.id
        })
        self.assertTrue(UserMembership.objects.filter(user=self.user, membership_type=self.membership_type).exists())