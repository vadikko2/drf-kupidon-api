from django.contrib.auth import models as auth_models
from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(null=False)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, null=False, blank=False)
    profile_order = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'images'
        app_label = 'profiles'


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        auth_models.User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    age = models.IntegerField(null=True)

    class Meta:
        db_table = 'profiles'
        app_label = 'profiles'
