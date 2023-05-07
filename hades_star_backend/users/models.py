import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from hades_star_backend.utils.soft_deletable_qs import SoftDeletableQS


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_queryset(self):
        """returns not deleted Users - common use"""
        return SoftDeletableQS(
            model=self.model, using=self._db, hints=self._hints
        ).filter(deleted_at__isnull=True)

    def get_deleted_users(self, **kwargs):
        """returns deleted Users"""
        return SoftDeletableQS(
            model=self.model, using=self._db, hints=self._hints
        ).filter(deleted_at__isnull=False)

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("EUSM1: The Email must be set"))
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Default user model
    User.objects.all() - returns not deleted users
    User.all_objects.all() - returns all users also deleted one
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    all_objects = models.Manager()

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    username = None
    email = models.EmailField(_("Email address"), unique=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    deleted_at = models.DateTimeField(null=True)

    def delete(self):
        """Softly delete object"""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def hard_delete(self):
        """Remove the object from the database permanently"""
        super().delete()

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def _if_email_taken_by_other_user(self, email):
        if email != self.email:
            return User.objects.filter(email=email).exists()
        return False

    def __str__(self):
        return f"{self.email}"
