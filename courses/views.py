from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .forms import RegisterForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Helper function to detect JSON request
def is_json_request(request):
    return request.headers.get('Content-Type') == 'application/json'

# ------------------------
# Auth Views
# ------------------------

@csrf_exempt
def register(request):
    if request.method == "POST":
        if is_json_request(request):
            data = json.loads(request.body)
            form = RegisterForm(data)
        else:
            form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if is_json_request(request):
                return JsonResponse({"message": "User registered successfully"})
            return redirect("course_list")
        else:
            if is_json_request(request):
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = RegisterForm()

    if is_json_request(request):
        return JsonResponse({"message": "Send POST with username and password"})
    return render(request, "registration/register.html", {"form": form})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        if is_json_request(request):
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if is_json_request(request):
                return JsonResponse({"message": f"Welcome {username}"})
            return redirect("course_list")
        else:
            if is_json_request(request):
                return JsonResponse({"error": "Invalid username or password"}, status=401)
            messages.error(request, "Invalid username or password.")

    if is_json_request(request):
        return JsonResponse({"message": "Send POST with username and password"})
    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    if is_json_request(request):
        return JsonResponse({"message": "Logged out successfully"})
    return redirect("login")


# ------------------------
# Course Views
# ------------------------

def course_list(request):
    courses = Course.objects.all()
    enrolled_courses = []

    if request.user.is_authenticated:
        enrolled_courses = Enrollment.objects.filter(student=request.user).values_list("course_id", flat=True)

    if is_json_request(request):
        data = [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "author": c.author,
                "duration": c.duration,
                "level": c.level,
                "enrolled": c.id in enrolled_courses
            }
            for c in courses
        ]
        return JsonResponse(data, safe=False)

    return render(request, "courses/course_list.html", {
        "courses": courses,
        "enrolled_courses": enrolled_courses,
    })


@login_required
@csrf_exempt
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

    if is_json_request(request):
        if created:
            return JsonResponse({"message": f"Enrolled in {course.title}"})
        else:
            return JsonResponse({"message": f"Already enrolled in {course.title}"})

    if created:
        messages.success(request, f"🎉 You’ve been successfully enrolled in {course.title}!")
    else:
        messages.info(request, f"✅ You’re already enrolled in {course.title}.")
    return redirect("my_courses")


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    if is_json_request(request):
        data = [
            {
                "course_id": e.course.id,
                "title": e.course.title,
                "enrolled_at": e.enrolled_at
            } for e in enrollments
        ]
        return JsonResponse(data, safe=False)

    return render(request, "courses/my_courses.html", {"enrollments": enrollments})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    if is_json_request(request):
        data = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "author": course.author,
            "duration": course.duration,
            "level": course.level,
            "is_enrolled": is_enrolled
        }
        return JsonResponse(data)

    context = {
        "course": course,
        "is_enrolled": is_enrolled,
    }
    return render(request, "courses/course_detail.html", context)
