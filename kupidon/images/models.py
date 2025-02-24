from django.contrib.auth import models as auth_models
from django.db import models


def profile_images_upload_to(instance, filename):
    return f'profile_images/{instance.user.username}/{filename}'


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField(upload_to=profile_images_upload_to, null=False, blank=False)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, null=False, blank=False)
    profile_order = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        return self.file.url

    class Meta:
        db_table = 'images'
        app_label = 'profiles'
        ordering = ["profile_order", "-created_at"]
