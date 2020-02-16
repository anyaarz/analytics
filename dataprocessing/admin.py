from django.contrib import admin
from .models import Domain, Items, Relation
from django.contrib.admin.models import LogEntry
admin.site.register(LogEntry)

admin.site.register(Domain)
admin.site.register(Items)
admin.site.register(Relation)

# Register your models here.
