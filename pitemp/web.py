import json
import os
from os.path import dirname, join

from pitemp import get_config
from MySQLdb import connect
from flask import Flask, render_template, jsonify, request, abort

from pitemp.db import execute
from pitemp.logger import get_temperature

BASE_DIR = dirname(dirname(__file__))

app = Flask('tempi', template_folder=join(BASE_DIR, 'templates'),
            static_folder=join(BASE_DIR, 'static'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/temperature')
def current_temperature():
    c, f = get_temperature()
    return jsonify({'celsius': c, 'fahrenheit': f})


@app.route('/data')
def get_data():
    location = request.args.get('location')
    interval = request.args.get('interval', 'hour').upper()
    if interval not in ['HOUR', 'MINUTE']:
        raise abort(400)

    sql = 'SELECT AVG(celsius), AVG(fahrenheit), reading_time FROM readings'
    data = {}
    if location:
        sql += ' WHERE location = %(location)s'
        data['location'] = location

    sql += ' GROUP BY {}(reading_time)'.format(interval)
    sql += ' ORDER BY reading_time DESC LIMIT 0, 12'

    result = {}
    for celsius, fahrenheit, time in execute(sql, data, True):
        result[time.strftime('%H:00')] = {
            'celsius': round(celsius, 2),
            'fahrenheit': round(fahrenheit, 2),
        }
    return jsonify(result)


@app.route('/locations')
def get_locations():
    sql = 'SELECT DISTINCT(location) FROM readings'
    data = [location[0] for location in execute(sql, None, True)]
    return jsonify({'data': data})


if __name__ == '__main__':
    DEBUG = get_config('debug', False)
    HOST = get_config('webserver', {})['host']
    PORT = get_config('webserver', {})['port']
    app.run(HOST, PORT, DEBUG)
