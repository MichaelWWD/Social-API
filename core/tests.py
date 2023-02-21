from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

class UserAuthentication(APITestCase):

    # endpoints needed
    register_url = "/api/auth/users/"
    activate_url = "/api/auth/users/activation/"
    login_url = "/api/auth/jwt/create/"
    user_details_url = "/api/auth/users/me/"

    # user information
    user_data = {
        "email": "test@example.com", 
        "username": "test_user", 
        "password": "verysecret"
    }
    login_data = {
        "username": "test_user", 
        "password": "verysecret"
    }

    def test_authentication_flow_with_email(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be sent
        self.assertEqual(len(mail.outbox), 1)
        
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        # you can print email to check it
        # print(mail.outbox[0].subject)
        # print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("access" in response.json())
        token = response.json()["access"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], self.user_data["email"])
        self.assertEqual(response.json()["username"], self.user_data["username"])
