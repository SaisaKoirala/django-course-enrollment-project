from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path("courses/enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path("my-courses/", views.my_courses, name="my_courses"),
]
