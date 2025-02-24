from django.contrib import admin


class ImageAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'profile_order', 'url')
    search_fields = ('user__username',)
