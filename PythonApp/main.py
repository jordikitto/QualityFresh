from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton
from gmplot import gmplot
from csv_parser import get_latitudes_and_longitudes

class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

        #Definition of the forms fields
        self._import_button = ControlButton("Import POI csv")
        self._show_map = ControlButton("Show Map")
        
        #Set actions
        self._show_map.value = self.__show_map_action

    def distance(self, P1, P2):
        """
        This function computes the distance between 2 points defined by
        P1 = (x1,y1) and P2 = (x2,y2) 
        """

        return ((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2) ** 0.5


    # Optimised path algorithm
    def optimized_path(self, coords, start=None):
        """
        This function finds the nearest point to a point
        coords should be a list in this format coords = [ [x1, y1], [x2, y2] , ...] 

        """
        if start is None:
            start = coords[0]
        pass_by = coords
        path = [start]
        pass_by.remove(start)
        while pass_by:
            nearest = min(pass_by, key=lambda x: self.distance(path[-1], x))
            path.append(nearest)
            pass_by.remove(nearest)
        return path

    def __show_map_action(self):
        # GET POI data
        poi_data = get_latitudes_and_longitudes('poi.csv')

        # sort POI data
        #poi_data.sort(key=lambda key: [key[1], key[0]])

        # define a start point
        start = [poi_data[0][0], poi_data[0][1]]

        # get the optimised path
        path = self.optimized_path(list(poi_data), start)

        # Place map
        gmap = gmplot.GoogleMapPlotter(poi_data[0][0], poi_data[0][1], 10)

        # Scatter and plot POI data
        top_attraction_lats, top_attraction_lons = zip(*path)
        gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False) #draw dots
        gmap.plot(top_attraction_lats, top_attraction_lons, 'red', edge_width=1) #draw lines between dots

        # Place markers and add label for visit ordering
        counter = 0
        for lat_long_data in path:
            counter = counter + 1
            lat, lon = lat_long_data
            gmap.marker(lat, lon, title=str(counter)) # place the marker

        # Draw
        gmap.draw("my_map.html")


class MissonControl(BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

if __name__ == '__main__':
    # Start the application
    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)
