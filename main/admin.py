from django.contrib import admin

from .models import AdvUser, Profile, Feedback
# Register your models here.

admin.site.register(AdvUser)
admin.site.register(Profile)
admin.site.register(Feedback)