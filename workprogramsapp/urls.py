from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path, re_path
from .views import WorkPrograms, WorkProgramsPost, WorkProgramsPostUpdate

urlpatterns = [
    path('workprograms/', WorkPrograms.as_view(), name='workprograms'),
    path('workprograms/newbinding', WorkProgramsPost.as_view(), name='author_update'),
    #ToDo: сделать нормально.
    #re_path(r'^workprograms/(?P<pk>)/update/', WorkProgramsPostUpdate.as_view(), name='workprograms_update'),
    url(r'^workprograms/(?P<pk>\d+)/update/$', WorkProgramsPostUpdate.as_view(), name='workprograms_update'),

]
