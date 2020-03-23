from django.test import Client, TestCase
from django.contrib.auth.models import User
from applications.models import Application


class TestApplicationView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create(username='megauser', is_superuser=True)
        self.user_1 = User.objects.create(username='User_1')
        self.user_2 = User.objects.create(username='User_2')

    def test_can_create_new_app(self):
        print(self.superuser)
