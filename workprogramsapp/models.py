from django.db import models
from dataprocessing.models import Items


class WorkProgram(models.Model):
    prerequisites = models.ManyToManyField(Items, related_name='WorkProgramPrerequisites',
                                           through='PrerequisitesOfWorkProgram',)
    outcomes = models.ManyToManyField(Items, related_name='WorkProgramOutcomes', through='OutcomesOfWorkProgram',)
    title = models.CharField(max_length=1024)
    hoursFirstSemester = models.IntegerField(blank=True, null=True)
    hoursSecondSemester = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.title


class PrerequisitesOfWorkProgram(models.Model):

    class Meta:
        auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE)
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1,
    )


class OutcomesOfWorkProgram(models.Model):

    class Meta:
        auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE)
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1,
    )
