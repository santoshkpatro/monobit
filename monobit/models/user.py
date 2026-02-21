from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now

from monobit.models.base import BaseUUIDTimestampModel


class UserManager(BaseUserManager):
    def create_superuser(self, email_address, full_name, password=None):
        user = self.model(
            email_address=self.normalize_email(email_address),
            full_name=full_name,
            email_address_verified_at=now,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user


class User(BaseUUIDTimestampModel, AbstractBaseUser):
    email_address = models.EmailField(unique=True)
    full_name = models.CharField(max_length=256, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    email_address_verified_at = models.DateTimeField(blank=True, null=True)
    phone_number_verified_at = models.DateTimeField(blank=True, null=True)
    blocked_at = models.DateTimeField(blank=True, null=True)

    last_login = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.DateTimeField(blank=True, null=True)

    password_expired_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"

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
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    @property
    def is_email_address_verified(self):
        return self.email_address_verified_at is not None

    @property
    def is_phone_number_verified(self):
        return self.phone_number_verified_at is not None

    @property
    def is_blocked(self):
        return self.blocked_at is not None

    @property
    def is_password_expired(self):
        return self.password_expired_at is not None
