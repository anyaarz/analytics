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
from django.template.loader import render_to_string

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

''' 
    index to render the main page  
'''
@login_required
def index(request):
    # Render the HTML template index.html with the data in the context variable
    user_list = User.objects.all()
    num_domain = Domain.objects.all().count()
    num_items = Items.objects.filter(author = request.user).count()
    return render(
        request,
        'index.html',
        context={'num_domain':num_domain,'num_items':num_items,'user_list':user_list}
    )
''' 
    Relation Block
    post and edit relation views  
'''
def edit_relation(request, pk):
    # Render the HTML template to edit relations
    relation = get_object_or_404(Relation, pk=pk)
    if request.method == "POST":
        form = RelationForm(request.POST, instance=relation)
        if form.is_valid():
            relation = form.save(commit=False)
            form.save()
            item_id = Items.objects.get(name = form.cleaned_data['item1']).id
            item_relations = Relation.objects.filter(item1 = item_id)
            #item_relations.
            #item2_rel = Relation.objects.prefetch_related('item2')
            print(item_relations)
            
            items_2 = [ list(i.item2.all()) for i in item_relations ]
            print(items_2)
            for item in form.cleaned_data['item2']:
                print(item)
                if item in items_2:
                    print('relation already excist')
            
            return redirect('/relation/')
    else:
        form = RelationForm(instance=relation)
    return render(request, 'dataprocessing/edit_relation.html', {'form': form})

            #print(relation.item1)
            #print(relation.item2.all().count())
            #print(relation.relation)
def post_relation(request):
    # Render the HTML template to post relations
    if request.method == "POST":
        form = RelationForm(request.POST)
        if form.is_valid():
            """
                Добавление связи 'являются частями одного раздела'.

            """
            items_same_parent = list(form.cleaned_data['item2'])
            if len(items_same_parent) > 0:
                for item in items_same_parent:
                    q = form.cleaned_data['item2'].exclude(name = item)
                    item_id = Items.objects.get(name = item).id
                    relation = Relation(item1 = Items.objects.get(pk = item_id), relation = '5')
                    relation.save()
                    relation.item2.set(q)

            relation = form.save(commit=False)
            form.save()

            item = Items.objects.get(id = relation.item1.id)
            value = item.value
            item.value = int(value) + relation.item2.all().count()
            item.save()
            #data = Data(user = request.user, date = timezone.now(), change_msg = 'created', item = Items.objects.get(pk=relation.item1.id),
                #result = (relation.item1.id,relation.relation,relation.item2.id))
            #data.save()
            return redirect('/relation/')
    else:
        form = RelationForm()
    return render(request, 'dataprocessing/edit_relation.html', {'form': form})


@login_required
def post_value(request):
    # Render the HTML template items_list.html to evaluate items
    
    items_list = Items.objects.all()
    domain_list = Domain.objects.filter(user=request.user) 
    return render(request, 'dataprocessing/value.html',context={'items_list':items_list,'domain_list':domain_list,})

''' 
    Domain Block
    post and edit domain views  
'''
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

''' 
    Relation Block
    post and edit item views  
'''
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
            return redirect('/evaluate/')
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
            if not Items.objects.filter(name = form.cleaned_data['item']).exists():
                items = form.save(commit=False)
                items.author = request.user 
                form.save()

            data = Data(user = request.user, date = timezone.now(),
                        change_msg = 'created', item = Items.objects.get(pk=items.id),
                        result = items)
            data.save()
            data.save()
            return redirect('/evaluate/')
    else:
        form = ItemsForm()
    #else: 
     #   raise Http404("У вас нет прав!")
    return render(request, 'dataprocessing/edit_items.html', {'form': form})
def item_delete(request, pk):
        items = Items.objects.get (pk = pk)
        items.delete()
        return redirect('/items/')
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
            return render(request, 'registration/login.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'dataprocessing/register.html', {'user_form': user_form})

''' 
    File Upload Block
    views for uploading keywords via txt file
'''
def upload(request):
    if request.method == 'POST':
        try:
            data = handle_uploaded_file(request.FILES['file'], str(request.FILES['file'])).splitlines()
            print(data)
            items_list = []
            for i in data:
                items_list.extend(i.split(','))
            domain_id = Domain.objects.get(name = request.POST.get("domain")).id
            for i in items_list:
                if Items.objects.filter(name = i).exists():
                    continue;
                else:
                    item = Items(name = i, domain = Domain.objects.get(pk=domain_id), 
                        author = request.user, source = 'uploaded')
                    item.save()  
            return redirect('/evaluate/')   
        except:
            return HttpResponse("Вы не добавили файл")
    return HttpResponse("Что-то не так, вернитесь обратно и повторите")

import os
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    with open('upload/' + filename, encoding = 'utf-8') as f:
        data=f.read()
    return data
        
