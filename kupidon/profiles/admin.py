from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'age', 'user__first_name', 'user__last_name')
    search_fields = ('user__username',)

    def has_delete_permission(self, request, obj=None):
        return False


class ImageAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'profile_order', 'url')
    search_fields = ('user__username',)
