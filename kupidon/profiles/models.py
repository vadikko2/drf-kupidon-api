from django.contrib.auth import models as auth_models
from django.contrib.gis.db import models as geo_models
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
    birthdate = models.DateField(null=True, default=None, blank=True)
    last_location = geo_models.PointField(
        geography=True,
        spatial_index=True,
        default=None,
        null=True,
        blank=True,
        srid=4326,
    )
    profile_image = models.URLField(null=True, blank=True, default=None)
    security_level = models.FloatField(null=True, blank=True, default=None)
    description = models.CharField(max_length=100, default='', blank=True)

    class Meta:
        db_table = 'profiles'
        app_label = 'profiles'
