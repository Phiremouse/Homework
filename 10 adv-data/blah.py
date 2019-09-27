from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#get latest date a reading was taken
#take the last date and return on the value as string
latest_date = session.query(func.max(Measurement.date)).scalar()
#converts the string to a datetime datatype Type
#The people who made the datetime module also named their class datetime
latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')


earliest_date = latest_date - dt.timedelta(days=365)
#Perform a query to retrieve the data and precipitation scores
# results = session.query(Measurement.date, Measurement.prcp)\
#    .filter((Measurement.date <= latest_date) & (Measurement.date >= earliest_date)).order_by(Measurement.date).all()


# df = pd.DataFrame(results)
# df=df.set_index('date')
# myplt = df.plot()

# #https://codeyarns.com/2015/06/29/how-to-hide-axis-of-plot-in-matplotlib/
# cur_axes = plt.gca()
# cur_axes.axes.get_xaxis().set_ticklabels([])


Sresults = session.query(Measurement.date, Measurement.tobs)\
    .filter((Measurement.date <= latest_date) & (Measurement.date >= earliest_date)& (Measurement.station=='USC00519281')).order_by(Measurement.date).all()

dfs = pd.DataFrame(Sresults)
dfs=dfs.set_index('date')
# myplts = dfs.plot(kind = 'hist', bins=12)


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
templookup = calc_temps('2012-02-28', '9999-99-99')
# z = list(templookup[0])
# xx=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= '2012-02-28').filter(Measurement.date <= '2012-03-05').all()
