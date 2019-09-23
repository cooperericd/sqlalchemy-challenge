import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date_end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a Dictionary using 
    #date as the key and prcp as the value.
    #Return the JSON representation of your dictionary
    session = Session(engine)
    dprec = [Measurement.date, Measurement.prcp]
    results = session.query(*dprec).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()

    date_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        date_precip.append(precip_dict)
    
    return jsonify(date_precip)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    session = Session(engine)
    stations = session.query(Station.station)
    session.close()

    station_list = []
    for station in stations:
        station_list.append(station)
        
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    session = Session(engine)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()

    date_temp = []
    for date, tobs in temps:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        date_temp.append(temp_dict)
    
    return jsonify(date_temp)

@app.route("/api/v1.0/start_date")
def start_date():
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    session = Session(engine)
    temps_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-07-01').all()
    session.close()

    temps_start_list = []
    for i in temps_start:
        temps_start_list.append(i)

    return jsonify(temps_start_list)

@app.route("/api/v1.0/start_date_end_date")
def start_date_end_date():
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    session = Session(engine)
    temps_stend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-07-01').filter(Measurement.date <= '2017-07-14').all()
    session.close()

    temps_stend_list = []
    for i in temps_stend:
        temps_stend_list.append(i)

    return jsonify(temps_stend_list)
    

if __name__ == "__main__":
    app.run(debug=True)