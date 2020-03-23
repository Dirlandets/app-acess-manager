from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from applications.models import Application


class TestApplicationModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='owner')
        self.app = Application.objects.create(owner=self.user, name='TestApp')

    def test_name_is_required(self):
        '''Username is required'''
        with self.assertRaises(IntegrityError):
            Application.objects.create()

    def test_api_key_is_created(self):
        '''Api key created automaticaly when istance created'''
        self.assertTrue(self.app.api_key)

    def test_refresh_api_key(self):
        '''Application.refresh_key() work as expected'''
        key = self.app.api_key
        self.app.refresh_key()
        self.assertNotEqual(self.app.api_key, key)

    def test_owner_is_obligatory(self):
        with self.assertRaises(IntegrityError):
            Application.objects.create(name='TestApp2')
