# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import CustomToken

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance, created, **kwargs):
#     if created:
#         CustomToken.objects.create(user=instance)
