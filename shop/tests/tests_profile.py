from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password123')
        self.client.login(username='user', password='password123')

    def test_profile_view_authenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_profile_view_get(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_edit_profile_view_post(self):
        response = self.client.post(reverse('edit_profile'), {'first_name': 'name1', 'last_name': 'name2', 
                                                              'email': 'example@gmail.com'})
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'name1')