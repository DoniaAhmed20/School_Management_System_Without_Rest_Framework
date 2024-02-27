from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
from django.contrib import admin
# from .models import Course


class Course(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    teacher = models.ForeignKey(User, related_name='courses_taught', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # Add this line

    def save(self, *args, **kwargs):
        # Ensure a teacher can teach only one active course
        if not self.pk:  
            if Course.objects.filter(teacher=self.teacher, active=True).exists():
                raise ValidationError('The selected teacher already has an active course.')
            else:
                self.active = True
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(User, related_name='enrollments_as_student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.course.active:
            super().save(*args, **kwargs)


class CourseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(user_type="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course, CourseAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(user_type="student")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Enrollment, EnrollmentAdmin)



