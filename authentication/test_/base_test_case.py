from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import User

class BaseTest(TestCase):
    """ This is the base class for all the tests """

    def setUp(self):
        self.client = APIClient()
        self.baseUrl = 'http://localhost:8000'
        self.user_data = {
            "user": {
                "username": "jacob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
            }
        }

