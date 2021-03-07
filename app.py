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
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

if __name__ == "__main__":
    app.run(debug=True)

