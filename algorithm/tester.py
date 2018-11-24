from math import *

distlist = [[1, 2],
            [3, 4],
            [5, 6]]

distlist = [[-24.9158511, 151.9281969],
            [-24.9102859, 151.9448466],
            [-24.9208587, 151.9371144],
            [-24.924378, 151.9460397],
            [-24.92599,  151.9340919],
            [-24.8745237, 151.8708398],
            [-24.8855635, 151.9122206],
            [-24.8950951, 151.9094754],
            [-24.9025067, 151.8989704]]



def haversine_distance(assetA, assetB):
    # we convert from decimal degree to radians
    latA, longA, latB, longB = map(radians, [assetA[0], assetA[1], assetB[0], assetB[1]])
        
    delta_lon = longB - longA
    delta_lat = latB - latA
        
    a = sin(delta_lat/2)**2 + cos(latA) * cos(latB) * sin(delta_lon/2)**25
    c = 2 * asin(sqrt(a))
        
    # approximate radius of the Earth: 6371 km
    return c * 6371
        

for x in distlist:
    coords = []
    subcoords = []
    for y in distlist:
        subcoords.append(haversine_distance(x, y))
    coords.append(subcoords)
    print(coords)
