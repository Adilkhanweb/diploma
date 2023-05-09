from django.contrib import admin
from .models import (
    Student,
    User,
    Teacher,
    Profile, Moderator, Consultation
)

# Register your models here.
admin.site.register(User)
admin.site.register(Consultation)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Moderator)
admin.site.register(Profile)
