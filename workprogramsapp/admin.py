from django.contrib import admin
from .models import WorkProgram, OutcomesOfWorkProgram, PrerequisitesOfWorkProgram


admin.site.register(WorkProgram)
admin.site.register(OutcomesOfWorkProgram)
admin.site.register(PrerequisitesOfWorkProgram)

