import numpy as np
import pandas as pd
import datetime as dt

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= prev_year).all()
    # Return a JSON list of temperature observations (TOBS) for the previous year.

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run(debug=True)