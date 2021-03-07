import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, date, time, timedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Bring over from jupyternotebook to setup database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect db into new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# save a reference for the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Setup Flask
app = Flask(__name__)

# Routes
# Welcome Route/Home page
@app.route("/")
def index():
    return (
        f"Welcome to Hawaii Climate API<br/>"
        f"Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/temp/start/end'>start/end</a><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
     # Query precipitation data
    prec_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation_data = []
    for date, prcp in prec_results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Query list of stations data
    stat_results = session.query(Station.station, Station.name).all()

    session.close()

    station_list = []
    for station, name in stat_results:
        station_dict = {}
        station_dict["Station ID"] = station
        station_dict["Station Name"] = name

        station_list.append(station_dict)
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= prev_year).all()

    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

session.close()

if __name__ == '__main__':
    app.run(debug=True)