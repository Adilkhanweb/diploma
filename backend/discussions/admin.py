from django.contrib import admin

from discussions.models import Discussion, Reply, Vote

# Register your models here.
admin.site.register(Discussion)
admin.site.register(Reply)
admin.site.register(Vote)
