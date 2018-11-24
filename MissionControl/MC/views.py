from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from io import TextIOWrapper
import csv

def index(request):  
    return render(request, 'MC/test_map.html', {'testVar':"Hi Jordi"})

def handle_uploaded_file(f):
    coordinates = []
    with TextIOWrapper(f, encoding='utf-8', newline='') as text_file:
        for row in csv.DictReader(text_file):
            coordinates.append([eval(row['Latitude']), 
                                eval(row['Longitude']), 
                                row['TaskType']])
    return coordinates

def upload_file(request):
    # Default
    latlong = [[27.4698, -153.0251]];

    # If Post
    if request.method == 'POST':
        data = request.POST.copy()
        form = UploadFileForm(request.POST)
        if not form.is_valid():
            title = data.get('title')
            latlong = handle_uploaded_file(request.FILES['file'])
            form.errors.clear()
            return render(request, 
                          'MC/playfile.html', 
                          {'form': form, 'latlong': latlong})
    else:
        form = UploadFileForm()
    return render(request, 
                  'MC/playfile.html', 
                  {'form': form, 
                   'latlong': latlong})