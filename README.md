# sqlalchemy-challenge

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

## Climate Analysis 
File name - climate_starter.jpynb

*  Use the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.
* Use SQLAlchemy create_engine to connect to your sqlite database.
* Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.
* Link Python to the database by creating an SQLAlchemy session.

## Climate App
File name - app.py

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

Use Flask to create your routes.
List all routes that are available.

* /api/v1.0/precipitation

* /api/v1.0/stations

* /api/v1.0/tobs

* /api/v1.0/<start> and /api/v1.0/<start>/<end>

## Bonus # 1
File name - temp_analysis_bonus_1_starter.jpynb

Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December? See analysis in jupyter notebook.