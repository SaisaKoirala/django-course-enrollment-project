from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course, Enrollment

class EnrollmentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="desc",
            author="Author",
            duration="5 hours",
            level="Beginner"
        )

    def test_enroll_view_requires_login(self):
        """Anonymous users should be redirected to login"""
        response = self.client.post(reverse("enroll_course", args=[self.course.id]))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/login/?next=/courses/enroll/{self.course.id}/")

    def test_enroll_authenticated_user(self):
        """Logged in user should be able to enroll"""
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("enroll_course", args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # redirected to "my-courses"
        self.assertTrue(Enrollment.objects.filter(student=self.user, course=self.course).exists())

    def test_double_enrollment(self):
        """User should not be enrolled twice"""
        self.client.login(username="testuser", password="password")
        # First enrollment
        self.client.post(reverse("enroll_course", args=[self.course.id]))
        # Second enrollment
        response = self.client.post(reverse("enroll_course", args=[self.course.id]))
        self.assertEqual(Enrollment.objects.filter(student=self.user, course=self.course).count(), 1)
