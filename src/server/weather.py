from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.db import get_db, add_data

bp = Blueprint('weather', __name__)


@bp.route('/')
def index():
    return 'Welcome to the homepage!'
    
    # db = get_db()
    # return render_template('weather/index.html')

@bp.route('/data', methods=('POST',))
def data(): 
    # Get the JSON data from the request
    data = request.get_json()
    # Print the data to the console
    print(data)
    # Save data to database
    add_data(data['Timestamp'], data['Temperature (C)'], 0, 0, 0, 0)

    # add_data(data['Timestamp'], data['Temperature (C)'], data['Pressure (Pa)'], data['Humidity (%)'], data['Air Quality (IAQ)'], data['eCO2 (ppm)'])  - full list 
    return 'JSON received!'
