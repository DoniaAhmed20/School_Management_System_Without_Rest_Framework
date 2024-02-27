from django.contrib import admin
from django.urls import path, include
from users.views import  register_view, login_view, home_view, logout_view, my_profile_view, update_profile
from courses.views import  index, enroll_course, my_courses, leave_course, courses_history
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token


# Create a router object
# router = DefaultRouter()
# # Register the viewsets with the router
# router.register(r'courses', CourseViewSet)
# router.register(r'enrollments', EnrollmentViewSet)
# router.register(r'users', UserViewSet)

urlpatterns = [
    # path('register/', register_view, name='register'),
#     path('api-auth/', include('rest_framework.urls')),
#     path('admin/', admin.site.urls),
# path('login/', UserLoginAPIView.as_view(), name='user-login'),
    #  path('dfw/', FBV_List.as_view()),
    # Detail view for GET, PUT, and DELETE requests with a specific ID
    # path('dfw/<int:pk>/', FBV_pk),
    # path('test/', FBV_List.as_view()),
    # path('test/<int:pk>/', FBV_List.as_view()),
    # path('test/<int:pk>/enroll/', FBV_List.as_view()),
    # path('search/', find_course, name='find_course'),
    #11 Token authentication
    # path('api-token-auth', obtain_auth_token),

# path('register/', UserRegistrationAPIView.as_view(), name='user_registration'),
# path('api/register/', UserRegistrationAPIView.as_view(), name='user_registration'),
    #  path('rest/fbv/<int:pk>',FBV_pkas_view()),

    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', index, name='home'),
    path('', index, name='home'),
    path('logout/', logout_view, name='logout'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('my-courses/', my_courses, name='my_courses'),
    path('leave-course/<int:course_id>/', leave_course, name='leave_course'),
    path('courses_history/', courses_history, name='courses_history'),
    path('my_profile/', my_profile_view, name='my_profile'),
    path('update-profile/', update_profile, name='update_profile'),
    
    # Include the router's URLs
    # path('', include(router.urls)),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
