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
            subcoords.append(round(haversine_distance(x[0:2], y[0:2]), 4))
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
        
    
def two_opt(route, distlist):
     best = route
     improved = True
     while improved:
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue # changes nothing, skip then
                    new_route = route[:]
                    new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                    if cost(new_route, distlist) < cost(best, distlist):
                         best = new_route
                         improved = True
          route = best
     return best

def main():
    distlist = [[-24.9158511, 151.9281969],
                [-24.9102859, 151.9448466],
                [-24.9208587, 151.9371144],
                [-24.924378, 151.9460397],
                [-24.925991, 151.9340919],
                [-24.8745237, 151.8708398],
                [-24.8855635, 151.9122206],
                ]
    
    # Distance Matrix
    distMat = dist_mat(distlist)
    
    # Visit list
    visitList = visit_list(distMat, 0)
    print(visitList)

    twoOpt = two_opt(visitList, distlist)
    
    print(twoOpt)


main()
