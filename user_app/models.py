from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class OwnUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("email is required")

        user = self.model(email=self.normalize_email(email), name=name)

        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.role = "admin"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_ROLE = (
        ("admin", "admin"),
        ("vendors", "vendors"),
        ("sponsor", "sponsor"),
        ("Guest", "Guest"),
    )

    name = models.CharField(max_length=144, verbose_name="name", default="name")
    email = models.EmailField(max_length=144, verbose_name="email address", unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(
        max_length=50, choices=USER_ROLE, verbose_name=("User Role")
    )

    objects = OwnUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # all admin is staff member
        return self.is_admin
