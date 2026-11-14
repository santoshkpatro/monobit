from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models, transaction

from monobit.models.base import BaseTimestampModel
from monobit.models.fields import PrefixedPrimaryKeyField
from monobit.models.choices import UserIdentityType


class User(BaseTimestampModel, AbstractBaseUser):
    id = PrefixedPrimaryKeyField(prefix="usr")
    username = models.CharField(max_length=128)
    email_address = models.EmailField(max_length=128)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    display_name = models.CharField(max_length=128, blank=True, null=True)
    identity_type = models.CharField(
        max_length=16, choices=UserIdentityType.choices, default=UserIdentityType.PERSON
    )
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email_address", "full_name"]

    class Meta:
        db_table = "users"
        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                name="uq_users_username",
            ),
            models.UniqueConstraint(
                fields=["email_address"],
                name="uq_users_email_address",
            ),
        ]

    @classmethod
    @transaction.atomic
    def create(cls, username, email_address, password, full_name):
        username = username.strip().lower()
        email_address = email_address.strip().lower()

        if cls.objects.filter(username=username).exists():
            raise ValidationError({"username": "Username already exists."})

        if cls.objects.filter(email_address=email_address).exists():
            raise ValidationError({"email_address": "Email already exists."})

        user = cls(
            username=username,
            email_address=email_address,
            full_name=full_name,
            display_name=full_name,
        )
        user.set_password(password)
        user.full_clean()
        user.save()

        return user
