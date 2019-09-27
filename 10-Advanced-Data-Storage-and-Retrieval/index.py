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
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine(r'sqlite:///C:\Users\User\Desktop\WUSTL201907DATA2\10-Advanced-Data-Storage-and-Retrieval\HomeWork\Instructions\Resources\hawaii.sqlite')
#C:\Users\User\Desktop\WUSTL201907DATA2\10-Advanced-Data-Storage-and-Retrieval\HomeWork\Instructions\Resources\hawaii.sqlite
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
       """List all available api routes."""
       return(
               f"Available Routes:<br/>"
               f"/api/v1.0/stations <br/>"
               f"/api/v1.0/precipitation <br/>"
               f"/api/v1.0/tobs <br/>"
               f"/api/v1.0/[start] <br/>"
               f"/api/v1.0/[start]/[end]<br/>"
               )

@app.route('/api/v1.0/stations')
def list_stations():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude,Station.elevation).all()
   session.close()
   all_stations=[]
   for id,station,name,lat,long,elv in results:
       station_dict = {}
       station_dict['id']=id
       station_dict['station']=station
       station_dict['name']=name
       station_dict['lat']=lat
       station_dict['long']=long
       station_dict['elv']=elv
       all_stations.append(station_dict)
   return jsonify(all_stations)

@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)    
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    earliest_date = latest_date - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter((Measurement.date <= latest_date) & (Measurement.date >= earliest_date)).order_by(Measurement.date).all()
    session.close()
    all_prcp=[]
    for date,prcp in results:
        temp_prcp={}
        temp_prcp['date']=date
        temp_prcp['prcp']=prcp
        all_prcp.append(temp_prcp)
    return jsonify(all_prcp)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    earliest_date = latest_date - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter((Measurement.date <= latest_date) & (Measurement.date >= earliest_date)).order_by(Measurement.date).all()
    session.close()
    all_tobs=[]
    for date,tobs in results:
        temp_tobs={}
        temp_tobs['date']=date
        temp_tobs['tobs']=tobs
        all_tobs.append(temp_tobs)
    return jsonify(all_tobs)

@app.route('/api/v1.0/<start>')
def juststart(start):
    session = Session(engine)
    def calc_temps(start_date, end_date):       
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()  

    results = calc_temps(start,'9999-99-99')
    session.close()
    tmin, tavg, tmax = results[0]
    all_data=[]
    for  tmin, tavg, tmax in results:
        temp_data={}
        temp_data['tminn']=tmin
        temp_data['tavg']=tavg
        temp_data['tmax']=tmax
        all_data.append(temp_data)
    return jsonify(all_data)

@app.route('/api/v1.0/<start>/<end>')
def startend(start,end):
    
    session = Session(engine)
    def calc_temps(start_date, end_date):       
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all() 

    results = calc_temps(start,end)
    session.close()
    tmin, tavg, tmax = results[0]
    all_data=[]
    for  tmin, tavg, tmax in results:
        temp_data={}
        temp_data['tminn']=tmin
        temp_data['tavg']=tavg
        temp_data['tmax']=tmax
        all_data.append(temp_data)
    return jsonify(all_data)
    

if __name__ == '__main__':
    app.run(debug=True)