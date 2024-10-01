from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.db import get_db, add_data, retrieve_data

import json

bp = Blueprint('weather', __name__)


@bp.route('/')
def index():
    return render_template('weather/index.html')

@bp.route('/visualise')
def visualise():
    return render_template('weather/visualise.html')

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
    # for row in results:
    #     print(row['temperature'])
    json_string = json.dumps(results)
    return json_string