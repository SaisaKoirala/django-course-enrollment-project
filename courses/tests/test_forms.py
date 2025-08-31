from django.test import TestCase
from courses.models import Course

class CourseFormTest(TestCase):
    def test_course_creation_form(self):
        course = Course.objects.create(title="AI Basics", description="Learn AI")
        self.assertEqual(course.title, "AI Basics")
