from django.contrib import admin

from images import admin as image_admin, models as image_models
from profiles import admin as profile_admins, models as profile_models

admin.site.site_header = 'Kupidon Administration'
admin.site.site_title = 'Kupidon'

admin.site.register(profile_models.Profile, profile_admins.ProfileAdmin)
admin.site.register(image_models.Image, image_admin.ImageAdmin)

__all__ = ('admin',)
