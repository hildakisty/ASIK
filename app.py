from flask import Flask
import folium
from flask import render_template
import os
from folium import plugins
import pickle



app = Flask(__name__)
model= pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/map', methods=['GET'])
def tracking():

    basemaps={
        'Google Satellite Hybrid':folium.TileLayer(
            tiles='https:mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite',
            overlay=True,
            control=True
        ),
    }
    d = os.path.dirname(os.path.abspath(__file__))
    start_coords = (-8.103, 110.431)
    wpp = "WPP 573"
    folium_map = folium.Map(location=start_coords, zoom_start=8)
    for basemap, tilelyr in basemaps.items():
        basemaps[basemap].add_to(folium_map)
    
    folium.LayerControl().add_to(folium_map)
    #fungsi mouse
    fmtr="function(num) {return L.Util.formation(num, 3) + '&deg;';};"
    plugins.MousePosition(position='topright', separator='|', lat_formatter=fmtr, lng_formatter=fmtr).add_to(folium_map)
    folium_map.add_child(folium.LatLngPopup())
    
    folium.Marker(location=[-6.929081337,105.808248],
                  popup="Koordinat:,SPL:, CHL:",
                  tooltip="See the details",
                  icon=folium.Icon(color='green',icon_color='yellow',icon='ship'),
                  draggable=True).add_to(folium_map)
    
    folium_map.save(d+'/templates/map.html')
    return render_template('index.html', koordinat = start_coords, wpp = wpp)
@app.route('/information')
def information():

    return render_template('information.html')

