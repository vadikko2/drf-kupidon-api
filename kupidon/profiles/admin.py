from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user__username',
        'birthdate',
        'last_location',
        'profile_image',
        'user__first_name',
        'user__last_name',
    )
    search_fields = ('user__username',)

    def has_delete_permission(self, request, obj=None):
        return False
