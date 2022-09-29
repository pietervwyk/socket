from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=False)
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://zlqcntsofqygzm:e59a3a6cf6a27c504fe282183ada49b1686e36ff7afacb77c854386a5bd66ac5@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/db7dqloivpuvco"
# app.server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:090909@localhost:5432/cars_api"
db = SQLAlchemy(app.server)
migrate = Migrate(app.server, db)

class Sensor_entry(db.Model):
    __tablename__ = 'sensor_table'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=False), nullable=True)
    wind = db.Column(db.Float(), nullable=True)
    temperature = db.Column(db.Float(), nullable=True)
    humidity = db.Column(db.Float(), nullable=True)
    uv = db.Column(db.Float(), nullable=True)
    

    def __init__(self, timestamp, wind, temperature, humidity, uv):
        self.timestamp = timestamp
        self.wind = wind
        self.temperature = temperature
        self.humidity = humidity
        self.uv = uv


app.layout = html.Div([
#     dcc.Interval(id='interval_pg', interval=1000, n_intervals=0),  
    html.H1(id='tag', children='hello'),
    html.Button('Send', id='button', n_clicks=0)
])

@app.callback(Output('tag', 'children'),
    [Input('button', 'n_clicks')])
def something(n_clicks):
    print('button clicked')
    new_row = Sensor_entry(timestamp=str(datetime.datetime.now()), wind=1.0, temperature=5.0, humidity=0, uv=2.0)
    db.session.add(new_row)
    db.session.commit()
    sensor_entries = Sensor_entry.query.all()
    df = pd.read_sql_table('sensor_table', con=db.engine)
    print(df)
    print(sensor_entries)
    return 'hello there'



#     new_car = CarsModel(name='whoo', model='letsgoo', doors=1)
#     db.session.add(new_car)
#     db.session.commit()
#     cars = CarsModel.query.all()

# class CarsModel(db.Model):
#     __tablename__ = 'cars'
# 
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     model = db.Column(db.String())
#     doors = db.Column(db.Integer())
# 
#     def __init__(self, name, model, doors):
#         self.name = name
#         self.model = model
#         self.doors = doors
# 
#     def __repr__(self):
#         return f"<Car {self.name}>"

# for your home PostgreSQL test table
# app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:your_password@localhost/test"

# for your live Heroku PostgreSQL database
# 

# db = SQLAlchemy(app.server)


# id = db.Column(db.DateTime(timezone=False), primary_key=True)
# timestamp = db.Column(db.DateTime(timezone=False), nullable=True)




# if __name__ == '__main__':
#     app.run_server(debug=True)