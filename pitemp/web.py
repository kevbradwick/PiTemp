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
    date = request.args.get('from')
    interval = request.args.get('interval', 'hour').upper()
    if interval not in ['HOUR', 'MINUTE']:
        raise abort(400)

    sql = 'SELECT AVG(celsius), AVG(fahrenheit), reading_time FROM readings'
    data = {}
    if date:
        sql = sql + ' WHERE reading_time > %(date)s'
        data['date'] = date

    sql = sql + ' GROUP BY {}(reading_time)'.format(interval)
    rows = execute(sql, data)
    print(rows)


if __name__ == '__main__':
    DEBUG = get_config('debug', False)
    HOST = get_config('webserver', {})['host']
    PORT = get_config('webserver', {})['port']
    app.run(HOST, PORT, DEBUG)
