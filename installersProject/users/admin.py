from django.contrib import admin
from .models import Profile
from django.utils.html import format_html


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', "profile_picture", 'phone_number']
    list_filter = ['user']
    search_fields = ['user__username']

    def profile_picture(self, obj):
        return format_html(f'<img src="/images/{obj.profile_image} "width="85" height="85""/>')


admin.site.register(Profile, ProfileAdmin)
