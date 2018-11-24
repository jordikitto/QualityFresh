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

 
                


def haversine_distance(assetA, assetB):
        coords = (*self.coords[assetA], *self.coords[cityB])
        # we convert from decimal degree to radians
        lat_cityA, lon_cityA, lat_assetB, lon_assetB = map(radians, coords)
        delta_lon = lon_assetB - lon_assetA
        delta_lat = lat_assetB - lat_assetA
        a = self.hav(delta_lat) + cos(lat_assetA) * cos(lat_cityB) * self.hav(delta_lon)
        c = 2 * asin(sqrt(a))
        # approximate radius of the Earth: 6371 km
        return c * 6371

def main():
    colnames = ['TaskID', 'TaskType', 'AssetCode', 'Field', 'Region', 'Latitude', 'Longitude', 'Elevation', 'CreateDate']
    dataPoints = pandas.read_csv('fuck.csv')
    dataList = []
    for row in dataPoints:
        dataList.append(row)
            
    #print(dataPoints)
    code = dataPoints.AssetCode.tolist()
    lat = numpy.array(dataPoints.Latitude.tolist())
    long = numpy.array(dataPoints.Longitude.tolist())
        
       # print(code)
       # print(lat)
       # print(long)
    coordinates = numpy.array((lat,long)).T   
       
    #coordinates = list(product(lat,long))
    print(coordinates)
    distances=[]
   
    for x in coordinates:   
        latA = x[0]
        longA = x[1]
        for y in coordinates:
            latB = y[0]
            longB = y[1]
            
            latA, longA, latB, longB = map(radians, [latA, longA, latB, longB ])
            delta_lon = longB - longA
            delta_lat = latB - latA
            a = sin(delta_lat/2)**2 + cos(latA) * cos(latB) * sin(delta_lon/2)**2
            c = 2 * asin(sqrt(a))* 6371
            # approximate radius of the Earth: 6371 km
            distances.append(c)
   # print (coordinates[0][1]) 
    
 
        
       
        
        
         
        
        
            
 
        
                
   

main()
 

#def getNeighbors(assetA, assetB):
#	distances = []
	
 #   for i in 
	#neighbors = []
	#for x in range(k):
#		neighbors.append(distances[x][0])
#	return neighbors
 
