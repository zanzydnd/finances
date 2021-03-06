from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class WalletUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, null=False, default="Wallet")
    is_email_verified = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "WalletUser"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UnverifiedUserCode(models.Model):
    user = models.ForeignKey(WalletUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    class Meta:
        db_table = "unverified_user_code"
        # verbose_name = "Пользователь"
        # verbose_name_plural = "Пользователи"


