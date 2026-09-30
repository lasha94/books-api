from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthFlowTests(APITestCase):
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(
            email="existing@example.com", password=self.password, first_name="Existing"
        )

    def test_register_success(self):
        payload = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "AnotherStrongPass123!",
            "password2": "AnotherStrongPass123!",
        }
        response = self.client.post(reverse("register"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_register_password_mismatch(self):
        payload = {
            "email": "mismatch@example.com",
            "password": "AnotherStrongPass123!",
            "password2": "Different123!",
        }
        response = self.client.post(reverse("register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password_rejected(self):
        payload = {
            "email": "weak@example.com",
            "password": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(reverse("register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        response = self.client.post(
            reverse("login"), {"email": self.user.email, "password": self.password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_auth(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get_and_update(self):
        login = self.client.post(
            reverse("login"), {"email": self.user.email, "password": self.password}
        ).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")

        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

        response = self.client.patch(reverse("profile"), {"first_name": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_logout(self):
        login = self.client.post(
            reverse("login"), {"email": self.user.email, "password": self.password}
        ).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")
        response = self.client.post(reverse("logout"), {"refresh": login["refresh"]})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_change_password(self):
        login = self.client.post(
            reverse("login"), {"email": self.user.email, "password": self.password}
        ).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")
        response = self.client.put(
            reverse("change_password"),
            {
                "old_password": self.password,
                "new_password": "BrandNewPass123!",
                "new_password2": "BrandNewPass123!",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("BrandNewPass123!"))

    def test_delete_account_requires_correct_password(self):
        login = self.client.post(
            reverse("login"), {"email": self.user.email, "password": self.password}
        ).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")

        response = self.client.delete(reverse("delete_account"), {"password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(reverse("delete_account"), {"password": self.password})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
