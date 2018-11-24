import csv

def get_latitudes_and_longitudes(filename):
	locations = []
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
		    locations.append([float(row['Latitude']), float(row['Longitude'])])
	# CSV is now closed
	return locations

#locations = get_latitudes_and_longitudes('poi.csv')
#print(locations[0][0])