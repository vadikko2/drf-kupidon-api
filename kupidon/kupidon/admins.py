from django.contrib import admin

from profiles import admin as profile_admins, models as profile_models

admin.site.site_header = 'Kupidon Administration'
admin.site.site_title = 'Kupidon'

admin.site.register(profile_models.Profile, profile_admins.ProfileAdmin)
admin.site.register(profile_models.Image, profile_admins.ImageAdmin)

__all__ = ('admin',)
