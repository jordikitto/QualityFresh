# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 11:18:52 2018

@author: gisel
"""
##from math import radians, cos, sin, asin, sqrt 
import csv
import random
from math import radians, cos, sin, asin, sqrt
import operator
from itertools import product
import pandas 
import numpy

def import_data(filename):
    colnames = ['TaskID', 'TaskType', 'AssetCode', 'Field', 'Region', 'Latitude', 'Longitude', 'Elevation', 'CreateDate']
    dataPoints = pandas.read_csv(filename)
    dataList = []
    for row in dataPoints:
        dataList.append(row)
            
    
    code = dataPoints.AssetCode.tolist()
    lat = numpy.array(dataPoints.Latitude.tolist())
    long = numpy.array(dataPoints.Longitude.tolist())
        
    distlist = numpy.array((lat,long)).T   
    return distlist
    

def haversine_distance(assetA, assetB):
    # we convert from decimal degree to radians
    latA, longA, latB, longB = map(radians, [assetA[0], assetA[1], assetB[0], assetB[1]])
    delta_lon = longB - longA
    delta_lat = latB - latA
    a = sin(delta_lat/2)**2 + cos(latA) * cos(latB) * sin(delta_lon/2)**25
    c = 2 * asin(sqrt(a))
    # approximate radius of the Earth: 6371 km
    return c * 6371
        
def dist_mat(distlist):
    coords = []
    for x in distlist:
        subcoords = []
        for y in distlist:
            subcoords.append(round(haversine_distance(x, y), 2))
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
        
    
    
    

def main():
   # distlist = [[-24.9158511, 151.9281969],
    #            [-24.9102859, 151.9448466],
     #           [-24.9208587, 151.9371144],
      #          [-24.924378, 151.9460397],
       #         [-24.92599,  151.9340919],
        #        [-24.8745237, 151.8708398],
         #       [-24.8855635, 151.9122206],
          #      [-24.8950951, 151.9094754],
           #     [-24.9025067, 151.8989704]]
    
    # Distance Matrix
    distlist = import_data('oof.csv')
    
    distMat = dist_mat(distlist)
    
    # Visit list
    visitList = visit_list(distMat, 3)
    print(visitList)
    return visitList
    

main()
 

        
       
        
        
         
        
        
            
 
        
                
   
