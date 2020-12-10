# -*- coding: utf-8 -*-
#%%
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from flask import Flask
#%%
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
#%%
app = Flask(__name__)
#%%

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f" Welcome! Here are available api routes:<br/r>"
        f"/api/v1.0/precipitation<br/r>"
        f"/api/v1.0/stations<br/r>"
        f"/api/v1.0/tobs<br/r>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

#%%
print('testing')
@app.route('/api/v1.0/precipitation')
def prcp():
    conn = engine.connect()
    query = f'''
        SELECT 
            date,
            AVG(prcp) as avg_prcp
        FROM
            measurement
        WHERE
            date >= (SELECT DATE(MAX(date),'-1 year') FROM measurement)
        GROUP BY
            date
        ORDER BY 
            date
    '''
    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.read_sql(query, conn)
    # Convert the date column to date
    prcp_df['date'] = pd.to_datetime(prcp_df['date'])
    # Sort the dataframe by date
    prcp_df.sort_values('date')
    prcp_json = prcp_df.to_json(orient='records')
    conn.close()
    return prcp_json

#%%
@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()
    query = '''
    SELECT
        s.station AS station_code,
        s.name AS station_name,
        COUNT(*) as station_count
    FROM
        measurement m
        INNER JOIN station s
        ON m.station = s.station
    GROUP BY 
        s.station,
        s.name
    ORDER BY
        station_count DESC
'''

    active_stations_df = pd.read_sql(query, conn)
    active_stations_df
    
    stations_json = active_stations_df.to_json(orient='records')
    conn.close()
    return stations_json 

#%%
@app.route("/api/v1.0/tobs")
def tobs():
    conn = engine.connect()
    query = f'''
    SELECT
        date,
        tobs
    FROM
        measurement
    WHERE
        date >= (SELECT DATE(MAX(date),'-1 year') FROM measurement)
        AND station = 'USC00519281'
    '''
    temp_obs_df = pd.read_sql(query, conn)
    temp_obs_df
    
    tobs_json = temp_obs_df.to_json(orient='records')
    conn.close()
    return tobs_json 
#%%
if __name__ == '__main__':
    app.run(debug=True)    
#%%
'''
/api/v1.0/precipitation
Convert the query results to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
/api/v1.0/stations
Return a JSON list of stations from the dataset.
'''