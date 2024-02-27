from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment,  User
from django.http import Http404
from .models import Course, Enrollment
from django.core.paginator import Paginator
from .models import Course, User
from django.utils import timezone

def index(request):
    # Retrieve active courses that have not ended
    active_courses = Course.objects.filter(active=True, end_date__gte=timezone.now().date())

    # Paginate the active courses
    # paginator = Paginator(active_courses, per_page=10)  # Assuming 10 items per page
    # page_number = request.GET.get('page')
    # paginated_courses = paginator.get_page(page_number)

    # Retrieve teachers
    teachers = User.objects.filter(user_type='teacher')

    # Render the template with paginated courses and teachers
    return render(request, 'home.html', {'courses': active_courses, 'teachers': teachers})

@login_required
def enroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        
        if not Enrollment.objects.filter(student=user, course=course).exists():
            if course.active:
                if course.start_date > timezone.now().date():
                    Enrollment.objects.create(student=user, course=course)
                    messages.success(request, 'You have successfully enrolled in the course.')
                else:
                    messages.error(request, 'You cannot enroll in this course as it has already started.')
            else:
                messages.error(request, 'This course is not active yet.')
        else:
            messages.info(request, 'You are already enrolled in this course.')
    
    return redirect('home')

@login_required
def my_courses(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == 'student':
            # Filter enrolled courses for students and exclude courses that have ended
            enrolled_courses = Enrollment.objects.filter(student=user, course__active=True, course__end_date__gte=timezone.now().date())
            return render(request, 'courses/my_courses.html', {'enrolled_courses': enrolled_courses})
        elif user.user_type == 'teacher':
            # Retrieve courses where the logged-in user is the teacher
            teacher_courses = user.courses_taught.filter(end_date__gte=timezone.now().date())
            return render(request, 'courses/my_courses.html', {'teacher_courses': teacher_courses})
    else:
        messages.error(request, 'You need to be logged in to view your courses.')
        return redirect('login')

@login_required
def leave_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        enrollment = Enrollment.objects.filter(student=user, course=course).first()
        if enrollment:
            if course.start_date > timezone.now().date():
                enrollment.delete()
                messages.success(request, 'You have left the course successfully.')
            else:
                messages.error(request, 'You cannot leave the course after the start date.')
        else:
            messages.error(request, 'You are not enrolled in this course.')
    return redirect('my_courses')

@login_required
def courses_history(request):
    # Get all enrollments of the current user
    user = request.user
    if user.is_authenticated:
        if user.user_type == 'student':
            # For students, get all enrollments of the current user
            enrollments = Enrollment.objects.filter(student=user)
            # Filter completed courses (courses whose end date has passed)
            completed_courses = [enrollment.course for enrollment in enrollments if enrollment.course.end_date < timezone.now().date()]
            return render(request, 'courses/courses_history.html', {'completed_courses': completed_courses})
        elif user.user_type == 'teacher':
            # For teachers, get all courses taught by the current user
            teacher_courses = user.courses_taught.all()
            # Filter completed courses (courses whose end date has passed)
            completed_teacher_courses = teacher_courses.filter(end_date__lt=timezone.now().date())
            return render(request, 'courses/courses_history.html', {'completed_courses': completed_teacher_courses})
    else:
        messages.error(request, 'You need to be logged in to view your course history.')
        return redirect('login')