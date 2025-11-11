from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from shop.models import Customer
from unittest.mock import patch

class TestAuthViews(TestCase):
    def setUp(self):
        self.password = "password123"
        self.user = User.objects.create_user(username="john", password=self.password)
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.signup_url = reverse("signup")
        self.homepage_url = reverse("homepage")

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_login_page_renders_template(self, mock_cart):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertIn("cart", response.context)

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_login_redirects_to_homepage(self, mock_cart):
        response = self.client.post(self.login_url, {"username": self.user.username, "password": self.password})

        self.assertRedirects(response, self.homepage_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_login_invalid_credentials_shows_error(self, mock_cart):
        response = self.client.post(self.login_url, {"username": self.user.username, "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("incorrect" in str(m) for m in messages_list))
        self.assertTemplateUsed(response, "login.html")

    def test_logout_redirectsand_clears_session(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.logout_url)
        messages_list = list(messages.get_messages(response.wsgi_request))

        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(any("successfully logged out" in str(m) for m in messages_list))

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_signup_page_renders_form(self, mock_cart):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertIn("form", response.context)

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_signup_creates_user_and_customer(self, mock_cart):
        response = self.client.post(self.signup_url, {
            "username": "newuser",
            "password1": "gfg#524!!G",
            "password2": "gfg#524!!G",
        })
        user = User.objects.get(username="newuser")

        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Customer.objects.filter(user=user).exists())

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_signup_invalid(self, mock_cart):
        response = self.client.post(self.signup_url, {
            "username": "baduser",
            "password1": "123",
            "password2": "321",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertFalse(User.objects.filter(username="baduser").exists())

    @patch("shop.views.get_cart_and_items", return_value=([], {}))
    def test_user_redirects_from_signup(self, mock_cart):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.signup_url)
        self.assertRedirects(response, reverse("profile"))

