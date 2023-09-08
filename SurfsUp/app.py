# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Ssession

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Model = automap_base()
Model.prepare(engine, reflect=True)

# reflect the tables
Model.classes.keys()

# Save references to each table
Measurement = Model.classes.measurement
Station = Model.classes.station

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
def home():
    print ("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

@app.route("/precipitation")
def precipitation():
    
    session = Session(engine)
    precipitation_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=year_ago).all()
    session.close()

    precipitation_data = {}
    for date, prcp in precipitation_query:
        precipitation_data[date] = prcp
    return jsonify(precipitation_data)

@app.route("date")
def date():
    session = Session(engine)
    date = session.query(Measurement.date).order_by(desc(Measurement.date))
    session.close()

    all_names = list(np.ravel(date))

    return jsonify(all_names)

@app.route("/station")
def station():
    session = Session(engine)
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()

    stations = list(np.ravel(active_stations))

    return jsonify(stations)
    

if __name__ == "__main__":
    app.run(debug=True)