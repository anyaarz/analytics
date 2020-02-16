from django import forms

from .models import WorkProgram, OutcomesOfWorkProgram, PrerequisitesOfWorkProgram


class WorkProgramOutcomesPrerequisites(forms.ModelForm):

    class Meta:
        model = WorkProgram
        #fields = ('id', 'prerequisites', 'outcomes', 'title')
        fields = '__all__'
