from django.contrib import admin

from .models import Ad, Comment

admin.site.register((Ad, Comment))
