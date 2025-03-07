import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func
import datetime

import pandas as pd
import numpy as np

class SQLHelper():
    #################################################
    # Database Setup
    #################################################

    def __init__(self):
        self.engine = create_engine("sqlite:///hawaii.sqlite")
        self.Base = None

        self.init_base()

    def init_base(self):
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)

    #################################################
    # Database Queries
    #################################################

    def query_precipitation_orm(self):
        # Save reference to the table
        Measurement = self.Base.classes.measurement

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Design a query to retrieve the last 12 months of precipitation data and plot the results.
        # Starting from the most recent data point in the database.

        # Calculate the date one year from the last date in data set.
        start_date = datetime.date(2016, 8, 23)

        # Perform a query to retrieve the data and precipitation scores
        results = session.query(Measurement.date, Measurement.station, Measurement.prcp).\
            filter(Measurement.date >= start_date).\
            order_by(Measurement.date.asc()).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        df2 = pd.DataFrame(results, columns=["Date", "Station", "Precipitation"])

        # Sort the dataframe by date
        df2["Date"] = pd.to_datetime(df2['Date'])
        df2 = df2.sort_values(by="Date", ascending=True).reset_index(drop=True)

        # close session
        session.close()

        data = df2.to_dict(orient="records")
        return(data)

        df = pd.read_sql(text(query), con = self.engine)
        data = df.to_dict(orient="records")
        return(data)

    def query_tobs_start_orm(self, start):
        # Save reference to the table
        Measurement = self.Base.classes.measurement

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')

        # Perform a query to retrieve the data and tobs scores
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        df2 = pd.DataFrame(results, columns=["min_tobs", "avg_tobs", "max_tobs"])

        # close session
        session.close()

        data = df2.to_dict(orient="records")
        return(data)
