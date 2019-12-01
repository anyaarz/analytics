from django.shortcuts import render, render_to_response,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse,Http404
from .models import User, Domain, Items, Data, Relation
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.utils import timezone
from django.views import generic
from .forms import UserRegistrationForm, DomainForm, ItemsForm, RelationForm, UploadFileForm
from django.contrib.auth.decorators import login_required, permission_required 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import random
''' 
    ItemsListView, RelationListView, DomainListView, DataListView 
    classes to generate a list items views 
'''
class ItemsListView(generic.ListView):
    model = Items
    def get_queryset(self):
        return Items.objects.all()

class RelationListView(generic.ListView):
    model = Relation
    def get_queryset(self):
        return Relation.objects.all()

class DomainListView(generic.ListView):
    model = Domain
    def get_queryset(self):
        return Domain.objects.all()

class DataListView(generic.ListView):
    model = Data
    def get_queryset(self):
        return Data.objects.all()


def index(request):
    # Render the HTML template index.html with the data in the context variable
    num_domain = Domain.objects.all().count()
    num_items = Items.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_domain':num_domain,'num_items':num_items}
    )

def edit_relation(request, pk):
    # Render the HTML template to edit relations
    relation = get_object_or_404(Relation, pk=pk)
    if request.method == "POST":
        form = RelationForm(request.POST, instance=relation)
        if form.is_valid():
            relation = form.save(commit=False)
            form.save()
            return redirect('/relation/')
    else:
        form = RelationForm(instance=relation)
    return render(request, 'dataprocessing/edit_relation.html', {'form': form})

def post_relation(request):
    # Render the HTML template to post relations
    if request.method == "POST":
        form = RelationForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            form.save()
            return redirect('/relation/')
    else:
        form = RelationForm()
    return render(request, 'dataprocessing/edit_relation.html', {'form': form})

def post_value(request):
    # Render the HTML template items_list.html to evaluate items
    items_list = Items.objects.all()
    random_items = random.sample(list(items_list), 2)
    if request.method == "POST":
        item1_id = Items.objects.get(name = request.POST.get("name")).id
        data = Data()
        relation = Relation()
        data.user = request.user
        data.date = timezone.now()
        data.change_msg = 'created'
        data.item = Items.objects.get(pk=item1_id)
        if request.POST.get("value"):
            data.action = 'value'
            data.result = request.POST.get("value")
        elif request.POST.get("relation"):
            item2_id = Items.objects.get(name = request.POST.get("name2")).id
            data.action = 'relation'
            relation.item1 = Items.objects.get(pk=item1_id) 
            relation.item2 = Items.objects.get(pk=item2_id) 
            relation.relation = request.POST.get("relation").split(' ')[0]
            relation.save()
            data.result = (Items.objects.get(name = request.POST.get("name")).id,
                request.POST.get("relation").split(' ')[0],
                Items.objects.get(name = request.POST.get("name2")).id)
        else:
            data.action = 'choice'
            data.result = request.POST.get("rand")
            print(random_items)
        data.save()
        return redirect("/create/")
    return render(request, 'dataprocessing/items_list.html',context={'items_list':items_list,'random_items':random_items})

@login_required
@permission_required('is_staff')
def post_domain(request):
    # Render the HTML template for superuser to create domain
    if request.method == "POST":
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            form.save()
            return redirect('/domain/')
    else:
        form = DomainForm()
    #else: 
     #   raise Http404("У вас нет прав!")
    return render(request, 'dataprocessing/edit_domain.html', {'form': form})

@login_required
@permission_required('is_staff')
def edit_domain(request, pk):
    # Render the HTML template to edit domain
    domain = get_object_or_404(Domain, pk=pk)
    if request.method == "POST":
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            domain = form.save(commit=False)
            form.save()
            return redirect('/domain/')
    else:
        form = DomainForm(instance = domain)
    return render(request, 'dataprocessing/edit_domain.html', {'form': form})

@login_required
def edit_item(request, pk):
    # Render the HTML template to edit items
    data = Data()
    items = get_object_or_404(Items, pk=pk)
    if request.method == "POST":
        form = ItemsForm(request.POST, instance=items)
        if form.is_valid():
            items = form.save(commit=False)
            items.author = request.user
            form.save()
            data.user = request.user
            data.date = timezone.now()
            data.change_msg = 'edited'
            data.item = Items.objects.get(pk=items.id)
            data.result = items
            data.save()
            return redirect('/create/')
    else:
        form = ItemsForm(instance = items)
    return render(request, 'dataprocessing/edit_items.html', {'form': form})
@login_required
def post_item(request):
    # Render the HTML template to post items
    if request.method == "POST":
        data = Data()
        form = ItemsForm(request.POST)
        if form.is_valid():
            items = form.save(commit=False)
            items.author = request.user
            form.save()
            data.user = request.user
            data.date = timezone.now()
            data.change_msg = 'created'
            data.item = Items.objects.get(pk=items.id)
            data.result = items
            data.save()
            return redirect('/create/')
    else:
        form = ItemsForm()
    #else: 
     #   raise Http404("У вас нет прав!")
    return render(request, 'dataprocessing/edit_items.html', {'form': form})

#get users domain
#d = Domain.objects.filter(user=request.user)
#print(d) 
def register(request):
    # Render the HTML template to register
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'dataprocessing/register.html', {'user_form': user_form})
'''
@csrf_protect
def handle_files(file):
    with open(file) as data_file:    
        data = json.load(data_file)
    return data


@csrf_exempt
def upload_file(request):
    print('Hi12')
    if request.method == 'POST':
        print('Hi')
        form = UploadFileForm(request.POST, request.FILES)
        print('Hi3')
        if form.is_valid():
            print('Hi4')
            d = handle_files(request.FILES['file'])
            print(d)
            item = Items()
            for key, values in data.items():
                item.domain = Domain.objects.get(key).id
            for i in values:
                item.name = i
                item.source = 'upload JSON file'
            item.save()
            print('items saved')
            form.save()
            return HttpResponseRedirect('/create/')
    else:
        form = UploadFileForm()
    return render(request,'dataprocessing/upload_file.html', {'form': form})
'''
def upload(request):
    if request.method == 'POST':
        data = handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        variable = data.split(':')[0]
        items_list = data.split(':')[1].split(',')
        for i in items_list:
            item = Items()
            item.name = i
            try:
                item.domain_id = Domain.objects.get(name=variable).id
            except:
                pass
            item.author = request.user
            item.source = 'uploaded'
            item.save()
        return redirect('/create/')

    return HttpResponse("Failed")

import os
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        print('path')
        os.mkdir('upload/')
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    with open('upload/' + filename) as f:
        data=f.read()
    print(data)
    return data
        
