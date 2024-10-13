import json

from flask import Blueprint, render_template, request

from server.db import add_data, retrieve_data
from server.graphs import default_graph, easy_linegraph

bp = Blueprint('weather', __name__)

@bp.route('/')
def index():
    return render_template('weather/index.html')

@bp.route('/visualise')
def visualise():
    return render_template('weather/visualise.html', easy_linegraph=easy_linegraph)

@bp.route('/analyse') 
def analyse():
    return render_template('weather/analyse.html')

@bp.route('/data', methods=('POST', ))
def post_data(): 
    data = request.get_json()
    print(data)
    add_data(data['Timestamp'], data['Temperature'], data['Pressure'], data['Humidity'], data['Air Quality'], data['eCO2'])  
    return 'JSON received!'

@bp.route('/data', methods=('GET',))
def get_data(): 
    # Get the JSON data from the SQL database
    results = retrieve_data()
    results = [dict(row) for row in results]
    json_string = json.dumps(results)
    return json_string

@bp.route('/test_graph', methods=('GET',))
def display_graph():
    return default_graph()


@bp.route('/graph/<weather_component>')
def display_weather_data(weather_component):
    weather_dict = {'humidity': 'Humidity %', 
    'temperature': 'Temperature C', 
    'pressure': 'Pressure Pa', 
    'air_quality': 'IAQ', 
    'eCO2': 'eCO2 ppm'}
    return easy_linegraph(weather_component, 
    weather_dict[weather_component]) 