# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:04:29 2023

@author: adria
"""

cityList = []
coordList = []
popList = []
distanceList = []
facilities = []
###############################################################################
# This function reads from the file miles.dat and loads information from this
# file into the data structures cityList, coordList, popList, and distanceList.
# This function does not return anything; it simply modifies these 4 lists
# in-place. The function assumes that all 4 lists are empty before the 
# function is called.
###############################################################################
def loadData(cityList, coordList, popList, distanceList):
    f = open("miles.dat")
    #cityList = []
    #coordList = []
    #popList = []
    #distanceList = []
    tempDistList = []
    for line in f:
        if ("A" <= line[0]) and (line[0] <= "Z"):
            pieces = line.split(",")
            cityList.append(pieces[0] + pieces[1].split("[")[0])
            coordList.append([int(pieces[1].split("[")[1]), int(pieces[2].split("]")[0])])
            popList.append(int(pieces[2].split("]")[1]))
            ###########
            tempDistList.reverse()
            distanceList.append(tempDistList)
            tempDistList = []
        elif (line[0].isdigit()):
            string = line.strip()
            s = string.split()
            for line in s:
                tempDistList.append(int(line))
    distanceList.remove(distanceList[0])
    tempDistList.reverse()
    distanceList.append(tempDistList)

###############################################################################
# This function returns the list containing the latitude and longitude of the
# city name. You can assume that name is a string of the form “cityName stateName”
# that appears in cityList.    
###############################################################################
def getCoordinates(cityList, coordList, name):
    index = cityList.index(name)
    latLong = coordList[index]
    return latLong
    
###############################################################################
# This function returns the population of the city name. You can assume that 
# name is a string of the form “cityName stateName” that appears in cityList. 
###############################################################################   
def getPopulation(cityList, popList, name):
    index = cityList.index(name)
    cityPop = popList[index]
    return cityPop

###############################################################################
# This function returns the distance between the two cities name1 and name2. 
# You can assume that name1 and name2 are strings of the form “cityName stateName” 
# that appear in cityList.
###############################################################################
def getDistance(cityList, distanceList, name1, name2):
    index1 = cityList.index(name1)
    index2 = cityList.index(name2)
    if index2 > index1:
        #lastInt = index1 + (len(distanceList[index2])-1)
        distance = distanceList[index2][index1]
    elif index1 > index2:
        #lastInt = index2 + (len(distanceList[index1])-1)
        distance = distanceList[index1][index2]
    elif index1 == index2:
        distance = 0
    
    return distance

###############################################################################
# This function returns the list of all cities with r miles of the city name. 
# You can assume that the city name is a string of the form “cityname statename” 
# that appears in cityList. You can assume that r is a nonnegative floating 
# point number. The list of cities returned by your function should be in the 
# same order as they appear in cityList.
###############################################################################

def nearbyCities(cityList, distanceList, name, r):
    result = [] #list that will be returned
    index = cityList.index(name) #indexes name EX: B = 2
    for j in (range(len(distanceList[index]))): #for loop to append anything behind the name
        if (distanceList[index][j] <= r): #if statement to determine if the int is less than or equal to r
            result.append(cityList[j]) #appends it to result list
    for i in (range(len(distanceList))): #for loop to append anything in front of name
        if (len(distanceList[i]) > index): #if statement to make sure list is not out of range
            if ((distanceList[i][index] <= r)): #if statement to determine if the in is less tna or equak to r
                result.append(cityList[i]) #appends it to result list
    
    return result

###############################################################################
#
# return number of unserved cities in range r of city with name
#
###############################################################################
def numNotServed(served, cityList, distanceList, name, r):
    citiesNear = nearbyCities(cityList, distanceList, name, r)
    count = 0
    for city in citiesNear:
        cityIndex = cityList.index(city)
        if served[cityIndex] == False:
            count += 1
    if served[cityList.index(name)] == False:
        count += 1
    return count
###############################################################################
#
# return city that can return the most cities within range r. If no further 
# cities to serve, return None
#
###############################################################################
def nextFacility(served, cityList,distanceList, r):
    maxCitiesToServe = 0
    facilityCity = None
    for city in cityList:
        if numNotServed(served, cityList, distanceList, city, r) > maxCitiesToServe:
            facilityCity = city
            maxCitiesToServe = numNotServed(served, cityList, distanceList, city, r)
    return facilityCity
###############################################################################
#
# This function returns a list consisting of cities at which facilities are 
# located such that every one of the 128 cities in cityList is at most r miles 
# (representing the radius of coverage) from a facility. The list of cities 
# returned by this function should be in the same order as they appear in cityList.
#
###############################################################################
def locateFacilities(cityList, distanceList, r):
    #initialize list served
    served = [False] * len(cityList)
    #initialize list to hold cities where service facilities will be
    facilities = []
    facility = nextFacility(served, cityList, distanceList, r)
    while (facility != None):
        #mark city in facility as served
        facilities.append(facility)
        index = cityList.index(facility)
        served[index] = True
        #mark cities served by this facility as served
        citiesNear = nearbyCities(cityList, distanceList, facility, r)
        for city in citiesNear:
            cityIndex = cityList.index(city)
            served[cityIndex] = True
        #get next best service facility w/ nextFacility
        facility = nextFacility(served, cityList, distanceList, r)
    
    return facilities

###############################################################################
#
# This function takes the cities in the list facilities and places push pins 
# at these cities.
#
###############################################################################
#fac300 = locateFacilities(cityList, distanceList, 300)
#fac800 = locateFacilities(cityList, distanceList, 800)
def display(facilities, cityList, distanceList, coordList):
    # open a new file for writing
    f = open("visualization300.kml", "w")
    # begin the kml code
    f.write('<Document>')
    
    # gets all facility in range 300
    fac300 = locateFacilities(cityList, distanceList, 300)
    # for loop that goes throug every facility in fac300
    for facility in fac300:
        # assings the id "redPin" to have the color red
        f.write('<Style id="redPin">')
        f.write('<IconStyle>')
        # hex value for a color
        f.write('<color>ff0000ff</color>')
        f.write('</IconStyle>')
        f.write('</Style>')
        
        # assings the id "orangePin" to have the color blue
        f.write('<Style id="orangePin">')
        f.write('<IconStyle>')
        # hex value for a color
        f.write('<color>ff0080ff</color>')
        f.write('</IconStyle>')
        f.write('</Style>')
        
        # places pin at facility
        index = cityList.index(facility)
        f.write('<Placemark>')
        # makes facility pins red
        f.write('<styleUrl>redPin</styleUrl>')
        f.write('<name>'+cityList[index]+'</name>')
        f.write('<Point>')
 
        # getting correct version of coordinates for facilities
        formattedLong = '-'+str(coordList[index][1])[:-2]+'.'+str(coordList[index][1])[-2:]
        formattedLat = str(coordList[index][0])[:-2]+'.'+str(coordList[index][0])[-2:]
        
        f.write('<coordinates>'+formattedLong+','+formattedLat+',0</coordinates>')
        f.write('</Point>')
        f.write('</Placemark>')
        
    # for loop that goes through every city
    for city in cityList:
        # determines if city is a facility
        if city not in fac300:
            closestFacility = None
            shortestDistance = 9999999
            # finds the nearest facility to the city given
            for facility in fac300:
                if ((getDistance(cityList, distanceList, city, facility)) < shortestDistance):
                    closestFacility = facility
                    shortestDistance = getDistance(cityList, distanceList, city, facility)
        
            cityIndex = cityList.index(city)
            closestIndex = cityList.index(closestFacility)
            # getting correct version of coordinates for city and nearest facility
            formattedLongCity = '-'+str(coordList[cityIndex][1])[:-2]+'.'+str(coordList[cityIndex][1])[-2:]
            formattedLatCity = str(coordList[cityIndex][0])[:-2]+'.'+str(coordList[cityIndex][0])[-2:]
            formattedLongNear = '-'+str(coordList[closestIndex][1])[:-2]+'.'+str(coordList[closestIndex][1])[-2:]
            formattedLatNear = str(coordList[closestIndex][0])[:-2]+'.'+str(coordList[closestIndex][0])[-2:]
            
            # places pin at city
            f.write('<Placemark>')
            # makes city pins orange
            f.write('<styleUrl>orangePin</styleUrl>')
            f.write('<name>'+city+'</name>')
            f.write('<Point>')
            f.write('<coordinates>'+formattedLongCity+','+formattedLatCity+',0</coordinates>')
            f.write('</Point>')
            f.write('</Placemark>')
            
            # write line
            f.write('<Style id="whiteLine">')
            f.write('<LineStyle>')
            # hex value for a color
            f.write('<color>ffffffff</color>')
            f.write('</LineStyle>')
            f.write('</Style>')
            
            # makes line connection from city to nearest facility
            f.write('<Placemark>')
            f.write('<name>Edge</name>')
            f.write('<description>A white line: To nearest facility</description>')
            # makes line white
            f.write('<styleUrl>#whiteLine</styleUrl>')
            f.write('<LineString>')
            f.write('<coordinates>'+formattedLongNear+','+formattedLatNear+',0'+','+formattedLongCity+','+formattedLatCity+',0''</coordinates>')
            f.write('</LineString>')
            f.write('</Placemark>')

    f.write('</Document>')    
     
    # close file
    f.close()
    
###############################################################################   
    # open a new file for writing
    g = open("visualization800.kml", "w")
    # begin the kml code
    g.write("<Document>")
    
    # gets all facility in range 800
    fac800 = locateFacilities(cityList, distanceList, 800)
    # for loop that goes throug every facility in fac800
    for facility in fac800:
        # assings the id "redPin" to have the color red
        g.write('<Style id="redPin">')
        g.write('<IconStyle>')
        # hex value for a color
        g.write('<color>ff0000ff</color>')
        g.write('</IconStyle>')
        g.write('</Style>')
        
        # assign the id "orangePin" to have the color orange
        g.write('<Style id="orangePin">')
        g.write('<IconStyle>')
        # hex value for a color
        g.write('<color>ff0080ff</color>')
        g.write('</IconStyle>')
        g.write('</Style>')
        
        # places pin at facility
        index = cityList.index(facility)
        g.write('<Placemark>')
        # makes facility pins red
        g.write('<styleUrl>redPin</styleUrl>')
        g.write('<name>'+cityList[index]+'</name>')
        g.write('<Point>')
 
        # getting correct version of coordinates for facilities
        formattedLong = '-'+str(coordList[index][1])[:-2]+'.'+str(coordList[index][1])[-2:]
        formattedLat = str(coordList[index][0])[:-2]+'.'+str(coordList[index][0])[-2:]
        
        g.write('<coordinates>'+formattedLong+','+formattedLat+',0</coordinates>')
        g.write('</Point>')
        g.write('</Placemark>')
        
    # for loop that goes through all cities
    for city in cityList:
        # checks if city is a facility
        if city not in fac800:
            closestFacility = None
            shortestDistance = 9999999
            # for loop that finds the nearest facility to the given city
            for facility in fac800:
                if ((getDistance(cityList, distanceList, city, facility)) < shortestDistance):
                    closestFacility = facility
                    shortestDistance = getDistance(cityList, distanceList, city, facility)
        
            cityIndex = cityList.index(city)
            closestIndex = cityList.index(closestFacility)
            # getting correct version of coordinates city and nearest facility
            formattedLongCity = '-'+str(coordList[cityIndex][1])[:-2]+'.'+str(coordList[cityIndex][1])[-2:]
            formattedLatCity = str(coordList[cityIndex][0])[:-2]+'.'+str(coordList[cityIndex][0])[-2:]
            formattedLongNear = '-'+str(coordList[closestIndex][1])[:-2]+'.'+str(coordList[closestIndex][1])[-2:]
            formattedLatNear = str(coordList[closestIndex][0])[:-2]+'.'+str(coordList[closestIndex][0])[-2:]
            
            # places pin at city
            g.write('<Placemark>')
            # makes city pin orange
            g.write('<styleUrl>orangePin</styleUrl>')
            g.write('<name>'+city+'</name>')
            g.write('<Point>')
            g.write('<coordinates>'+formattedLongCity+','+formattedLatCity+',0</coordinates>')
            g.write('</Point>')
            g.write('</Placemark>')
            
            # write line
            g.write('<Style id="whiteLine">')
            g.write('<LineStyle>')
            # hex value for a color
            g.write('<color>ffffffff</color>')
            g.write('</LineStyle>')
            g.write('</Style>')
            
            # makes line conncetion from city to nearest facility
            g.write('<Placemark>')
            g.write('<name>Edge</name>')
            g.write('<description>A white line: To nearest facility</description>')
            # makes line white
            g.write('<styleUrl>#whiteLine</styleUrl>')
            g.write('<LineString>')
            g.write('<coordinates>'+formattedLongNear+','+formattedLatNear+',0'+','+formattedLongCity+','+formattedLatCity+',0''</coordinates>')
            g.write('</LineString>')
            g.write('</Placemark>')
    
    g.write("</Document>")


    # close file
    g.close()

# creates kml files
loadData(cityList, coordList, popList, distanceList)
display(facilities, cityList, distanceList, coordList)



