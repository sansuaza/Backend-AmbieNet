#django 
from django.test import TestCase

from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

#Model
from AmbieNet.users.models import User

class LoginAPITestCase(APITestCase):
    """User login test case."""
    
    def setUp(self):
        """Test case setup, building de instances that are needes in the test case."""
        self.user = User.objects.create(
            username= 'saenzavs',
            email= 'saenz@mail.com',
            password= 'admin12345',
            phone_number= '31212231232',
            first_name= 'steven',
            last_name= 'saenz'
        )
        

        self.data = {
            'username': 'saenzavs',
            'password': 'admin12345'
        }

        self.url = '/users/login/'

    def test_code_generation(self):
        
        
        request = self.client.post(self.url, self.data)
  #import pdb; pdb.set_trace()     
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)