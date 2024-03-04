# from rest_framework import status
# from rest_framework.response import Response
# from .api_serializers import UserRegistrationSerializer
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import User
import os

def register_view(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        profile_image = request.FILES.get('profile_image')
        cv = request.FILES.get('cv')

        # Create user object
        user = User.objects.create_user(
            first_name = first_name,
            username=username,
            email=email,
            password=password,
            user_type=user_type,
            gender=gender,
            date_of_birth=date_of_birth,
            profile_image=profile_image,
            cv=cv
        )

        # Save the uploaded file to the media folder if profile_pic exists
        if profile_image:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'customer_images'))
            filename = fs.save(profile_image.name, profile_image)
        if cv:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'cv'))
            filename = fs.save(cv.name, cv)

        # Send email to admin
        admin_email = '09doniaahmed01@gmail.com'  # Replace with your admin email
        message = f'A new user {username} has registered and requires activation. Please activate the user.'
        send_mail(
            'New User Registration - Activation Required',
            message,
            '09doniaahmed01@gmail.com',  # Replace with your sender email
            [admin_email],
            fail_silently=True
        )


        # Construct URL to admin panel
        admin_panel_url = reverse('admin:index')

        # Render success page with admin panel link
        return redirect('home')

    # Render registration form template for GET requests
    return render(request, 'register.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)
        # print(user.is_authenticated)
        
        if user is not None:
            if user.is_active:
                # Log in the user using Django's standard login function
                login(request, user)

                # Redirect to the home page after successful login
                return redirect('home')  # Replace 'home' with the URL name of your home page
            else:
                messages.error(request, 'Your account is not active yet.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def home_view (request):
    return render(request, 'home.html')



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout, such as the home page
    return redirect('login') 

from django.contrib.auth.decorators import login_required

@login_required
def my_profile_view(request):
    user = request.user
    return render(request, 'my_profile.html', {'user': user})

from django.http import JsonResponse
@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        # Retrieve the data from the request.POST dictionary
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        profile_image = request.FILES.get('profile_image')
        cv = request.FILES.get('cv')

        # Update the user data
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender

        # Check if profile_image is provided and update it
        if profile_image:
            user.profile_image = profile_image

        # Check if cv is provided and update it
        if cv:
            user.cv = cv

        # Save the updated user
        user.save()

        # Redirect to the profile page after successful update
    #     return redirect('my_profile')

    # return render(request, 'update_profile.html')
    return JsonResponse({'status': 'success'})
    # return redirect('my_profile')
        
    # return render(request, 'register.html')
