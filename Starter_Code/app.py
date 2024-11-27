# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/mehmetakifcingoz/Desktop/Bootcamp/Module 10- Advenced SQL/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
	return (
		f"Welcome to the Climate API!<br/>"
		f"Available Routes:<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/start<br/>"
		f"/api/v1.0/start/end<br/>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	# Calculate the date 1 year ago from the last data point in the database
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
	one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

	# Perform a query to retrieve the data and precipitation scores
	results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

	# Convert the query results to a dictionary using date as the key and prcp as the value
	precipitation_data = {date: prcp for date, prcp in results}

	# Return the JSON representation of the dictionary
	return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
	# Query all stations
	results = session.query(Station.station).all()

	# Convert list of tuples into normal list
	stations_list = list(np.ravel(results))

	# Return the JSON list of stations
	return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
	# Calculate the date 1 year ago from the last data point in the database
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
	one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

	# Query the dates and temperature observations of the most active station for the last year of data
	results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == 'USC00519281').all()

	# Convert list of tuples into normal list
	tobs_list = list(np.ravel(results))

	# Return the JSON list of temperature observations (tobs) for the previous year
	return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
	# Perform a query to retrieve the data
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

	# Convert list of tuples into normal list
	start_list = list(np.ravel(results))

	# Return the JSON list of the minimum temperature, average temperature, and max temperature for a given start range
	return jsonify(start_list)
@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
	# Perform a query to retrieve the data
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	# Convert list of tuples into normal list
	start_end_list = list(np.ravel(results))

	# Return the JSON list of the minimum temperature, average temperature, and max temperature for a given start-end range
	return jsonify(start_end_list)

if __name__ == "__main__":
	app.run(debug=True)
