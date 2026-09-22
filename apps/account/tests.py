import re

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Account, School


class RegistrationAndActivationTests(TestCase):
    def _register(self):
        return self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'SuperSecret123!',
            'password2': 'SuperSecret123!',
            'date_of_birth': '2000-01-01',
        })

    def test_registration_creates_inactive_user_and_sends_activation_email(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/activate/', mail.outbox[0].body)

    def test_activation_link_activates_the_account(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        match = re.search(r'/activate/([^/]+)/([^/]+)/', mail.outbox[0].body)
        uidb64, token = match.group(1), match.group(2)

        self.client.get(f'/activate/{uidb64}/{token}/')

        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_invalid_activation_token_does_not_activate(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        match = re.search(r'/activate/([^/]+)/([^/]+)/', mail.outbox[0].body)
        uidb64 = match.group(1)

        self.client.get(f'/activate/{uidb64}/not-a-real-token/')

        user.refresh_from_db()
        self.assertFalse(user.is_active)


class LoginTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='existing@example.com', username='existing', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def test_login_with_correct_credentials_succeeds(self):
        # Regression test: AccountAuthenticationForm used to be a ModelForm
        # bound to Account, so Django ran Account.email's unique=True
        # validator on every login attempt - failing with "Account with
        # this Email already exists" for every real user, every time.
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'SuperSecret123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_wrong_password_fails_without_crashing(self):
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'SuperSecret123!',
        })
        self.assertNotIn('_auth_user_id', self.client.session)


class AccountUpdateTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='update@example.com', username='updateuser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.force_login(self.user)

    def test_get_renders_form_with_current_values(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['account_form'].instance, self.user)

    def test_post_actually_saves_changes(self):
        # Regression test: account_view used to have no POST handling at
        # all, so submitting this form was a silent no-op.
        response = self.client.post(reverse('account'), {
            'email': 'update@example.com',
            'username': 'renamed-user',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'renamed-user')

    def test_duplicate_email_is_rejected(self):
        Account.objects.create_user(
            email='taken@example.com', username='someoneelse', password='x'
        )
        response = self.client.post(reverse('account'), {
            'email': 'taken@example.com',
            'username': 'updateuser',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'update@example.com')


class SuperuserTests(TestCase):
    def test_create_superuser_is_active(self):
        # Regression test: create_superuser never set is_active=True, so a
        # freshly created superuser (is_active defaults to False on this
        # model) could not log in anywhere until manually fixed in the DB.
        admin = Account.objects.create_superuser(
            email='admin@example.com', username='admin', password='SuperSecret123!'
        )
        self.assertTrue(admin.is_active)


class SchoolDashboardTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Бишкек 5-мектеп')

        self.principal = Account.objects.create_user(
            email='principal@example.com', username='principal', password='SuperSecret123!'
        )
        self.principal.is_active = True
        self.principal.is_school_admin = True
        self.principal.school = self.school
        self.principal.save()

        self.teacher = Account.objects.create_user(
            email='teacher@example.com', username='teacher', password='SuperSecret123!'
        )
        self.teacher.is_active = True
        self.teacher.save(update_fields=['is_active'])

        self.client.login(email='principal@example.com', password='SuperSecret123!')

    def test_non_school_admin_is_redirected(self):
        self.client.logout()
        self.client.login(email='teacher@example.com', password='SuperSecret123!')
        resp = self.client.get(reverse('school_dashboard'))
        self.assertRedirects(resp, reverse('account'))

    def test_admin_can_view_dashboard(self):
        resp = self.client.get(reverse('school_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Бишкек 5-мектеп')

    def test_admin_can_add_existing_teacher_by_email(self):
        self.client.post(reverse('school_dashboard'), {
            'action': 'add_teacher', 'email': 'teacher@example.com',
        })
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.school_id, self.school.id)

    def test_adding_unknown_email_shows_error_and_adds_nobody(self):
        resp = self.client.post(reverse('school_dashboard'), {
            'action': 'add_teacher', 'email': 'nobody@example.com',
        }, follow=True)
        self.assertContains(resp, 'табылган жок')
        self.assertEqual(self.school.teachers.count(), 1)

    def test_cannot_add_teacher_already_in_another_school(self):
        other_school = School.objects.create(name='Ош 2-мектеп')
        self.teacher.school = other_school
        self.teacher.save(update_fields=['school'])

        resp = self.client.post(reverse('school_dashboard'), {
            'action': 'add_teacher', 'email': 'teacher@example.com',
        }, follow=True)
        self.assertContains(resp, 'башка мектепке таандык')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.school_id, other_school.id)

    def test_admin_can_remove_a_teacher(self):
        self.teacher.school = self.school
        self.teacher.save(update_fields=['school'])

        self.client.post(reverse('school_dashboard'), {
            'action': 'remove_teacher', 'teacher_id': self.teacher.id,
        })
        self.teacher.refresh_from_db()
        self.assertIsNone(self.teacher.school_id)
