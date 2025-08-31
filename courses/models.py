from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    video = models.FileField(upload_to="course_videos/", blank=True, null=True) 
    author = models.CharField(max_length=100, blank=True, default="Unknown", help_text="Enter author's name")
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., 5 hours, 3 weeks")
    level = models.CharField(max_length=50, blank=True, help_text="Beginner, Intermediate, Advanced")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
