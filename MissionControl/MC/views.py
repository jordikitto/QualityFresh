from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from io import TextIOWrapper
import csv

from math import *

def haversine_distance(assetA, assetB):
    # we convert from decimal degree to radians
    latA, longA, latB, longB = map(radians, [assetA[0], assetA[1], assetB[0], assetB[1]])
    delta_lon = longB - longA
    delta_lat = latB - latA
    a = sin(delta_lat/2)**2 + cos(latA) * cos(latB) * sin(delta_lon/2)**2   
    c = 2 * asin(sqrt(a))
    # approximate radius of the Earth: 6371 km
    return c * 6371
        
def dist_mat(distlist):
    coords = []
    for x in distlist:
        subcoords = []
        for y in distlist:
            subcoords.append(round(haversine_distance(x[0:2], y[0:2]), 2))
        coords.append(subcoords)
    return coords
        
def get_min(subList, blacklist):
    nextMin = 1000000
    nextIndex = -1;
    for x in range(len(subList)):
        if ((subList[x] < nextMin) and (x not in blacklist)):
            nextMin = subList[x]
            nextIndex = x
    return nextIndex

def visit_list(distMat, startIndex):
    # List of indeces to ignore for min
    path = [startIndex]

    # Go over the dist mat
    currIndex = startIndex
    currList = distMat[currIndex]
    
    for x in range(1, len(distMat)):
        currIndex = get_min(currList, path)
        path.append(currIndex)
        currList = distMat[currIndex]
    return path
        
   
def cost(route, distlist):
    distance = 0
    for x in route:
        y = x + 1
        if y == len(route):
            y = 0
        distance += haversine_distance(distlist[x], distlist[y])
    return distance


def split_visit(visitList, distlist, start):
    startLL = distlist[start]
    netdist = 0
    goback = []
    reset = False
    for x in range(1, len(visitList)):
        # Find the next point
        y = x - 1

        # update distance
        fromLL = distlist[y]
        if (reset):
            fromLL = startLL
        toLL = distlist[x]
        netdist += haversine_distance(toLL, fromLL)
        
        if (netdist > 600):
            # go back after we hit
            reset = True
            netdist = 0
            goback.append(y + 1)
        else:
            reset = False
    for index in reversed(goback):
        visitList.insert(index, start)    
    return visitList

def main(distlist):
    
    # Distance Matrix
    distMat = dist_mat(distlist)
    start =  0
    
    # Visit list
    visitList = visit_list(distMat, start)
    visitList = split_visit(visitList, distlist, start)

    # Get indeces of zeroes
    indexList = [i for i, e in enumerate(visitList) if e == start]
    indexList.append(len(visitList) + 1)

    # New latitude and longitude - based off 
    newLL = []
    for x in visitList:
        newLL.append(distlist[x])
    costList = [0]

    return [newLL, costList]



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
            [latlong, costList] = main(latlong)
            return render(request, 
                          'MC/playfile.html', 
                          {'form': form, 'latlong': latlong})
    else:
        form = UploadFileForm()
    return render(request, 
                  'MC/playfile.html', 
                  {'form': form, 
                   'latlong': latlong})