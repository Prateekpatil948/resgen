from django.contrib import admin
from .models import Profile
# Register your models here.
admin.site.site_header = "ResGen"
admin.site.site_title = " ResGen Resume Generator "
admin.site.index_title = "Resgen Administor"

admin.site.register(Profile)
