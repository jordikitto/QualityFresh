from django.http import HttpResponse
from django.shortcuts import render

def index(request):  
    return render(request, 'MC/test_map.html', {'testVar':"Hi Jordi"})