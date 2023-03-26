from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.get_full_name() + ' ' + self.email


class StudentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Students")
        return super().get_queryset(*args, **kwargs).filter(is_staff=False).filter(is_superuser=False).filter(
            groups__in=[group])


class TeacherManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Teachers")
        return super().get_queryset(*args, **kwargs).filter(is_staff=False).filter(is_superuser=False).filter(
            groups__in=[group])


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name="Students")
        self.groups.add(group)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name="Teachers")
        self.groups.add(group)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="uploads/", default="default/default-picture.jpg")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
