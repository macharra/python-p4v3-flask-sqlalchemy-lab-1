# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        body =earthquake.to_dict()
        status=200
         
    
    else:
        body = {'message': f'earthquake {id} not found.'}
        status = 404

    return make_response(body, status)
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter_by(magnitude=magnitude).all()
    count = len(earthquakes)

    if earthquakes:
        body = {'count': count, 'quakes': [quake.to_dict() for quake in earthquakes]}
        status = 200
    else:
        body = {'message': f'No earthquakes found with magnitude {magnitude}.'}
        status = 404

    return make_response(body, status)

# Add views here


if __name__ == '__main__':
    app.run(port=5000, debug=True)