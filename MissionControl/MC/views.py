from django.http import HttpResponse
from django.shortcuts import render



def index(request):  
    return render(request, 'MC/test_map.html', {'testVar':"Hi Jordi"})
	
def testpage(request):  
	context = ""
	context2 = ""
	
	if (request.method == 'POST'):
		print(request.POST.get("myFile", ""))
		print(type(request.POST.get("myFile", "")))
		context = str(type(request.POST.get("myFile", "")))
		context2 = request.POST.get("myTest", "")
		
	return render(request, 'MC/playfile.html', {'context': context, 'context2': context2})