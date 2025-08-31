from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Course, Enrollment


class CourseModelTest(TestCase):
    def test_course_str(self):
        course = Course.objects.create(
            title="Python Basics",
            description="Learn Python step by step"
        )
        self.assertEqual(str(course), "Python Basics")


class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student", password="test123")
        self.course = Course.objects.create(title="Django Basics", description="Intro course")

    def test_student_can_enroll(self):
        enrollment = Enrollment.objects.create(student=self.user, course=self.course)
        self.assertEqual(enrollment.student.username, "student")
        self.assertEqual(enrollment.course.title, "Django Basics")

    def test_duplicate_enrollment_not_allowed(self):
        Enrollment.objects.create(student=self.user, course=self.course)
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=self.user, course=self.course)
