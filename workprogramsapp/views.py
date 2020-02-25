from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views import View
from .models import WorkProgram, OutcomesOfWorkProgram, PrerequisitesOfWorkProgram
from .forms import WorkProgramOutcomesPrerequisites


from dataprocessing.models import Items
import itertools
# Create your views here.


class WorkPrograms(View):

    def get(self, request):

        workprograms = WorkProgram.objects.prefetch_related('outcomes', 'prerequisites')
        workprograms_outcomes = []
        workprograms_prerequisites = []

        for workprogram in workprograms:
            outcomes = [item.name for item in workprogram.outcomes.all()]
            outcomes_levels = OutcomesOfWorkProgram.objects.values_list('masterylevel').filter(workprogram=workprogram.pk)
            outcomes_levels2 = [entry for entry in outcomes_levels]
            outcomes_levels3 = []
            for outcome in outcomes:
                outcomes_levels3.append({'item': outcome, 'item_level': outcomes_levels2[outcomes.index(outcome)][0]})

            prerequisites = [item.name for item in workprogram.prerequisites.all()]
            prerequisites_levels2 = [entry for entry in PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
                workprogram=workprogram.pk)]
            prerequisites_levels3 = []
            for prerequisite in prerequisites:
                prerequisites_levels3.append({'item': prerequisite, 'item_level': prerequisites_levels2[prerequisites.index(prerequisite)][0]})
                workprograms_prerequisites.append({'title': workprogram.title, 'outcomes_levels': outcomes_levels3, })
            print(workprograms_outcomes)
            workprograms_outcomes.append({'pk': workprogram.pk, 'hoursFirstSemester': workprogram.hoursFirstSemester,
                                          'hoursSecondSemester': workprogram.hoursSecondSemester, 'title': workprogram.title, 'outcomes_levels': outcomes_levels3,
                                          'prerequisites_levels': prerequisites_levels3})

        return render(request, 'workprograms/workprograms.html', {'workprograms': workprograms_outcomes})


class WorkProgramsPost(View):

    def get(self, request):
        form = WorkProgramOutcomesPrerequisites()
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})

    def post(self, request):
        WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST)
        if WorkProgramOP.is_valid():
            WorkProgramOP.save()
            return redirect('workprograms')
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})


class WorkProgramsPostUpdate(View):

    def get(self, request, pk):
        wp_obj = get_object_or_404(WorkProgram, id=pk)
        form = WorkProgramOutcomesPrerequisites(instance=wp_obj)
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})

    def post(self, request, pk):
        wp_obj = get_object_or_404(WorkProgram, id=pk)

        if request.method == "POST":
            WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST, instance=wp_obj)
            if WorkProgramOP.is_valid():
                WorkProgramOP.save()
                return redirect('workprograms')
        else:
            WorkProgramOP = WorkProgramOutcomesPrerequisites(instance=wp_obj)
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})



