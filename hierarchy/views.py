
from .models import Designation
from django.shortcuts import render
from django.db import connection
from .forms import DesignationForm
from .forms import HierarchyForm
from .forms import SHierarchyForm
from django.shortcuts import redirect
from django.db import connection

# Create your views here.

def add_designation(request):
    
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('add_designation')
    else:
        form = DesignationForm()

    
    return render(request, 'hierarchy/add_designation.html', {'form': form})

def add_hierarchy(request):
    
    
    if request.method == "POST":
        
        form = HierarchyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            dat = form.cleaned_data['juniors']
            juniors = list(dat.values_list(flat=True))
            cursor = connection.cursor()
            cursor.execute("""SELECT juniors
            FROM hierarchy_designation
            WHERE name='%s' """ %name)
            data = cursor.fetchall()
            data = list(list(d) for d in data)
            
            existing_juniors = data[0]
            
            if existing_juniors[0] != '':
                juniors = list(set(juniors + existing_juniors))
            juniors_str = '*'.join([str(j) for j in juniors])
            juniors_str2 = "','".join([str(j) for j in juniors])
            
            cursor.execute("""UPDATE hierarchy_designation
            SET juniors='%s' WHERE name='%s'""" %(juniors_str,name))
            cursor.execute("""UPDATE hierarchy_designation
            SET superior='%s' WHERE id IN('%s')""" %(name,juniors_str2))
            return redirect('add_hierarchy')
    else:
        form = HierarchyForm()

    
    return render(request, 'hierarchy/add_hierarchy.html', {'form': form})

def show_hierarchy(request):
    
    if request.method == "POST":
        
        form = SHierarchyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            
            cursor = connection.cursor()
            cursor.execute("""SELECT juniors
            FROM hierarchy_designation
            WHERE name='%s' """ %name)
            data = cursor.fetchall()
            
            data = list(list(d) for d in data)
            juniors = data[0]
            
            if juniors[0] != '':
                
                temp = juniors[0].split('*')
                jnrs = list(set(temp))
            else:
                jnrs = juniors[0] 
                               
            juniors_str = "','".join(jnrs)
           
            
            cursor.execute("""SELECT name FROM hierarchy_designation
            WHERE id IN('%s')""" %juniors_str)
            dat = cursor.fetchall()
            
            dat = [d[0] for d in dat]
            juniors = dat
            

            cursor.execute("""SELECT name,superior FROM hierarchy_designation""")
            data = cursor.fetchall()
            name_superior = { str(r[0]):str(r[1]) for r in data}
            
            superiors = []
            temp_name = str(name)
            
            while name_superior[temp_name] != '':
                superiors.append(name_superior[temp_name])
                temp_name = name_superior[temp_name]
               
            
            form = {'data':{'dat1':juniors,'dat2':superiors}}
            
                
    else:
        form = SHierarchyForm()

    
    return render(request, 'hierarchy/show_hierarchy.html', {'form': form})
