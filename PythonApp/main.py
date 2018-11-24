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

    def __show_map_action(self):
        # GET POI data
        poi_data = get_latitudes_and_longitudes('poi.csv')

        # sort POI data
        poi_data.sort(key=lambda key: [key[1], key[0]])

        # Place map
        gmap = gmplot.GoogleMapPlotter(poi_data[0][0], poi_data[0][1], 10)

        # Scatter POI data
        top_attraction_lats, top_attraction_lons = zip(*poi_data)
        gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)
        gmap.plot(top_attraction_lats, top_attraction_lons, 'red', edge_width=1)

        # Marker
        counter = 0
        for lat_long_data in poi_data:
            counter = counter + 1
            lat, lon = lat_long_data
            gmap.marker(lat, lon, title=str(counter))

        # Draw
        gmap.draw("my_map.html")


class MissonControl(BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

if __name__ == '__main__':
    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)
