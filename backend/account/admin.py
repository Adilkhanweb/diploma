from django.contrib import admin
from .models import (
    Student,
    User,
    Teacher,
    Profile,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Profile)
