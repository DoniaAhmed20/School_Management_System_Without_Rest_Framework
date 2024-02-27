from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    date_of_birth = models.DateField()
    
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    # active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    # Add or change related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new user
            # Send email to admin
            send_mail(
                'New User Registration',
                f'A new user {self.username} has registered. Please activate the user.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],  # Replace with your admin email
                fail_silently=True,
            )
        super().save(*args, **kwargs)

# Custom token model
# class CustomToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

# # Signal to create a token for each user upon creation
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance, created, **kwargs):
#     if created:
#         # Check if a token already exists for the user
#         if not CustomToken.objects.filter(user=instance).exists():
#             # Create a new token for the user
#             CustomToken.objects.create(user=instance)
