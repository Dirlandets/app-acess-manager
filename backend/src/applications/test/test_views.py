from django.test import Client, TestCase
from django.contrib.auth.models import User
from applications.models import Application


class TestApplicationCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create(username='megauser', is_superuser=True)
        self.user_1 = User.objects.create(username='user1')
        self.user_2 = User.objects.create(username='user2')

    def test_superuser_can_create_new_app(self):
        self.client.force_login(self.superuser)
        response = self.client.post('/api/', {'name': 'TestApp', 'owner': self.superuser.pk})
        assert response.status_code == 201
        jsn = response.json()
        self.assertEqual(jsn['owner'], self.superuser.pk)

    def test_superuser_can_create_new_app_for_user(self):
        self.client.force_login(self.superuser)
        response = self.client.post('/api/', {'name': 'TestApp', 'owner': self.user_1.pk})
        assert response.status_code == 201
        jsn = response.json()
        self.assertEqual(jsn['owner'], self.user_1.pk)

    def test_user_can_create_new_app(self):
        self.client.force_login(self.user_1)
        response = self.client.post('/api/', {'name': 'TestApp', 'owner': self.user_1.pk})
        assert response.status_code == 201
        jsn = response.json()
        self.assertEqual(jsn['owner'], self.user_1.pk)

    def test_user_can_not_create_new_app_for_another_user(self):
        self.client.force_login(self.user_1)
        response = self.client.post('/api/', {'name': 'TestApp', 'owner': self.user_2.pk})
        assert response.status_code == 201
        jsn = response.json()
        self.assertEqual(jsn['owner'], self.user_1.pk)


class TestApplicationListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create(username='megauser', is_superuser=True)
        self.superuser_app = Application.objects.create(
            name='SuperuserApp',
            owner=self.superuser
        )
        self.user_1 = User.objects.create(username='user1')
        self.user_1_app = Application.objects.create(
            name='user_1_App',
            owner=self.user_1
        )
        self.user_2 = User.objects.create(username='user2')
        self.user_2_app = Application.objects.create(
            name='user_2_App',
            owner=self.user_2
        )

    def test_superuser_can_see_all_applications(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/')
        assert response.status_code == 200
        jsn = response.json()
        self.assertEqual(len(jsn), 3)

    def test_user_can_see_only_where_owner(self):
        self.client.force_login(self.user_1)
        response = self.client.get('/api/')
        assert response.status_code == 200
        jsn = response.json()
        self.assertEqual(len(jsn), 1)


class TestRetreveView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create(username='megauser', is_superuser=True)
        self.superuser_app = Application.objects.create(
            name='SuperuserApp',
            owner=self.superuser
        )
        self.user_1 = User.objects.create(username='user1')
        self.user_1_app = Application.objects.create(
            name='user_1_App',
            owner=self.user_1
        )
        self.user_2 = User.objects.create(username='user2')
        self.user_2_app = Application.objects.create(
            name='user_2_App',
            owner=self.user_2
        )

    def test_superuser_can_see_all(self):
        self.client.force_login(self.superuser)
        response = self.client.get(f'/api/{self.user_1_app.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_only_owned(self):
        self.client.force_login(self.user_2)
        response = self.client.get(f'/api/{self.user_1_app.pk}/')
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user_1)
        response = self.client.get(f'/api/{self.user_1_app.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_name_patch(self):
        self.client.force_login(self.user_1)
        response = self.client.patch(f'/api/{self.user_1_app.pk}/', {'name': 'NewName'}, content_type='application/json',)
        jsn = response.json()
        self.assertEqual(jsn['name'], 'NewName')

    def test_user_can_not_update_other_user_app_name_patch(self):
        self.client.force_login(self.user_1)
        self.client.patch(f'/api/{self.user_2_app.pk}/', {'name': 'NewName'}, content_type='application/json',)
        self.assertNotEqual(self.user_2_app.name, 'NewName')

    def test_can_not_directly_change_api_key(self):
        self.client.force_login(self.user_1)
        old_key = self.user_1_app.api_key
        response = self.client.patch(
            f'/api/{self.user_1_app.pk}/',
            {'api_key': 'ba54802c-0361-4eb7-9491-7109946b9f34'},
            content_type='application/json',
        )
        jsn = response.json()
        self.assertEqual(str(old_key), jsn['api_key'])

     
class TestUpdateToken(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create(username='megauser', is_superuser=True)
        self.superuser_app = Application.objects.create(
            name='SuperuserApp',
            owner=self.superuser
        )
        self.user_1 = User.objects.create(username='user1')
        self.user_1_app = Application.objects.create(
            name='user_1_App',
            owner=self.user_1
        )
        self.user_2 = User.objects.create(username='user2')
        self.user_2_app = Application.objects.create(
            name='user_2_App',
            owner=self.user_2
        )

    def test_can_refresh_token(self):
        self.client.force_login(self.user_1)
        old_key = self.user_1_app.api_key
        response = self.client.get(f'/api/{self.user_1_app.pk}/refresh/', content_type='application/json', follow=True)
        jsn = response.json()
        self.assertNotEqual(str(old_key), jsn['api_key'])

    def test_redirect_after_refresh_token(self):
        self.client.force_login(self.user_1)
        response = self.client.get(f'/api/{self.user_1_app.pk}/refresh/', content_type='application/json', follow=True)
        self.assertEqual(response.redirect_chain[0], (f'/api/{self.user_1_app.pk}/', 302))
