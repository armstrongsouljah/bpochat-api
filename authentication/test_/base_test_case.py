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
        self.valid_user = User.objects.create_user(
            username ='armstrongtest',
            email='armstrongtest@server.com',
            password='#Pho3nix9q'
        )
        self.valid_user_login = {
            "user":{
                "email":"armstrongtest@server.com",
                "password":"#Pho3nix9q"
            }
        }
        self.invalid_user_login = {
            "user":{
                "email":"armstrongtest@server",
                "password":"#Pho3nix9q"
            }
        }
