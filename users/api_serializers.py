# # serializers.py

# from rest_framework import serializers
# from .models import User

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username','first_name', 'last_name', 'email', 'password', 'user_type', 'gender', 'date_of_birth', 'cv', 'profile_image', 'enrollments_as_student']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
