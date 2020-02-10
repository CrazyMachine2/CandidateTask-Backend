from application import app, db, cities_schema, city_schema
from flask import url_for, redirect, request, jsonify
from flask_cors import cross_origin
from application.models import City
from application.constants import URL_TEMPLATE, METRIC, IMPERIAL, CITIES, TEMPERATURE, MAIN, MESSAGES
import requests

#Before first request
@app.before_first_request
def populate_cities():
    """ Pre-populates the city table if the application is started for the first time 

    If table is already pre-populated, the method is returning nothing.
    """
    if City.query.filter_by(name=CITIES[0]).first():
        return

    for city in CITIES:
        _add_city(city)

#Routes
@app.route('/api/cities')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_cities():
    cities = City.query.all()
    result = cities_schema.dump(cities)
    return jsonify(result)

@app.route('/api/city', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def add_city():
    city_name = request.get_json()['name'].lower().capitalize()
    return _add_city(city_name)

@app.route('/api/update', methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def update():
    _update_on_refresh()
    return jsonify(MESSAGES.get('SUCCESS'))


@app.route('/api/unique-name')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def is_name_taken():
    """Checks if name is taken"""
    name = request.args.get('name').lower().capitalize()
    city = City.query.filter_by(name=name).all()
    return jsonify(cities_schema.dump(city)) if city else jsonify([])

#Private methods
def _get_open_weather_requests(city_name):
    metric_url = URL_TEMPLATE % (city_name, METRIC)
    imperial_url = URL_TEMPLATE % (city_name, IMPERIAL)

    metric_resp = requests.get(metric_url)
    imperial_resp = requests.get(imperial_url)

    return (metric_resp, imperial_resp)

def _add_city(city_name):
    """ Adds a new city to the database. 
    """

    #Checks if city exist, if exist returns ALREADY_EXIST message
    if City.query.filter_by(name=city_name).first():
        return jsonify(MESSAGES.get('ALREADY_EXIST_MESSAGE'))

    metric_resp, imperial_resp = _get_open_weather_requests(city_name)

    #Checks if request is OK, if not returns UNSUCCESS message
    if not metric_resp:
        return jsonify(MESSAGES.get('UNSUCCESS'))

    metric_json = metric_resp.json()
    imperial_json = imperial_resp.json()
    new_city = City(name=city_name, temp_celsius=int(metric_json[MAIN][TEMPERATURE]), temp_fahrenheit=int(imperial_json[MAIN][TEMPERATURE]))

    #Adds and commits to the database
    db.session.add(new_city)
    db.session.commit()
    return jsonify(MESSAGES.get('SUCCESS'))

def _update_on_refresh():
    """ Updates all the temperatures of all cities in the database 
    """
    cities = City.query.all()

#Iterates over all cities in the database and updates their value
    for city in cities:
        metric_resp, imperial_resp = _get_open_weather_requests(city.name)

        metric_json = metric_resp.json()
        imperial_json = imperial_resp.json()

        city.temp_celsius = int(metric_json[MAIN][TEMPERATURE])
        city.temp_fahrenheit = int(imperial_json[MAIN][TEMPERATURE])
    db.session.commit()
