from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import math

NUM_VEHICLES = 4

class OrToolsRouter(object):
	def __init__(self, lat_long_data):
		self._data = lat_long_data
		self._routed_data = []
		self._home = None

	def create_data_model(self):
		"Store the data for the problem"
		data = {}
		# Set locations data
		home = self._data[0] # home is first point
		self._home = home
		rel_data = []
		# Update coordinates to be relative to home instead
		for points in self._data:
			rel_to_home_point = (points[0] - home[0]), (points[1] - home[1])
			rel_data.append(rel_to_home_point)
		_locations = rel_data
		data["locations"] = [(l[0], l[1]) for l in _locations]
		data["num_locations"] = len(data["locations"])
		data["num_vehicles"] = NUM_VEHICLES # TO FIGURE OUT
		data["depot"] = 0
		return data

	def calculate_distance(self, pos_1, pos_2):
		"Compute distance between two lat-long positions"
		#return math.sqrt((pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_1[1])**2)
		def distance(lat1, lon1, lat2, lon2):
			p = 0.017453292519943295     #Pi/180
			a = 0.5 - math.cos((lat2 - lat1) * p)/2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
			return 12742 * math.asin(math.sqrt(a)) #2*R*asin...
		return distance(pos_1[0], pos_1[1], pos_2[0], pos_2[1])
		# UPDATE: curvature of earth using (gdal) - talk about

	def create_distance_callback(self, data):
		"""Creates callback to return distance between points."""
		_distances = {}

		for from_node in range(data["num_locations"]):
			_distances[from_node] = {}
			for to_node in range(data["num_locations"]):
				if from_node == to_node:
					_distances[from_node][to_node] = 0
				else:
					_distances[from_node][to_node] = (
						self.calculate_distance(data["locations"][from_node],
										data["locations"][to_node]))

		def distance_callback(from_node, to_node):
			"""Returns the distance between the two nodes"""
			return _distances[from_node][to_node]

		return distance_callback

	def add_distance_dimension(self, routing, distance_callback):
		"""Add Global Span constraint"""
		distance = 'Distance'
		maximum_distance = 600  # Maximum distance per vehicle.
		routing.AddDimension(
			distance_callback,
			0,  # null slack
			maximum_distance,
			True,  # start cumul to zero
			distance)
		distance_dimension = routing.GetDimensionOrDie(distance)
		# Try to minimize the max distance among vehicles.
		distance_dimension.SetGlobalSpanCostCoefficient(100)

	###########
	# Printer #
	###########
	def print_solution(self, data, routing, assignment):
		"""Print routes on console."""
		print("##############SOLUTION#############")
		total_distance = 0
		for vehicle_id in range(data["num_vehicles"]):
			index = routing.Start(vehicle_id)
			plan_output = 'Route for trip {}:\n'.format(vehicle_id)
			distance = 0
			route = []
			while not routing.IsEnd(index):
				plan_output += ' {} ->'.format(routing.IndexToNode(index))
				previous_index = index
				# Get node data
				node_index = routing.IndexToNode(index)
				route.append(data["locations"][node_index])
				index = assignment.Value(routing.NextVar(index))
				#distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
				print(routing.GetArcCostForVehicle(previous_index, index, vehicle_id))
				if (index < len(data["locations"])):
					curr_pos = data["locations"][index]
					if previous_index < len(data["locations"]):
						prev_pos = data["locations"][previous_index]
						the_dist = self.calculate_distance(prev_pos, curr_pos)
						distance += the_dist
						print("Dist: "+str(the_dist) + " km")
			plan_output += ' {}\n'.format(routing.IndexToNode(index))
			plan_output += 'Distance of route: {} km\n'.format(distance)
			print(plan_output)
			total_distance += distance
			self._routed_data.append(route)
		print('Total distance of all routes: {} km'.format(total_distance))

	########
	# Main #
	########
	def run(self):
		"""Entry point of the program"""
		# Instantiate the data problem.
		data = self.create_data_model()
		# Create Routing Model
		routing = pywrapcp.RoutingModel(
			data["num_locations"],
			data["num_vehicles"],
			data["depot"])
		# Define weight of each edge
		distance_callback = self.create_distance_callback(data)
		routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
		self.add_distance_dimension(routing, distance_callback)
		# Setting first solution heuristic (cheapest addition).
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC) # pylint: disable=no-member
		# Solve the problem.
		assignment = routing.SolveWithParameters(search_parameters)
		if assignment:
			self.print_solution(data, routing, assignment)

	def get_routed_data(self):
		return_data = self._routed_data
		for index in range(len(self._routed_data)):
			return_data[index] = [(l[0] + self._home[0], l[1] + self._home[1]) for l in self._routed_data[index]]
		return return_data
	