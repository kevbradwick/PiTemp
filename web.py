import os
from flask import Flask, render_template, Response, jsonify


app = Flask('tempi')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/temperature')
def current_temperature():
    return jsonify({'celcius': 12.3, 'farenheit': 45.32})


if __name__ == '__main__':
    DEBUG = os.environ.get('DEBUG', '0') == '1'
    HOST = os.environ.get('TEMPI_HOST', '0.0.0.0')
    PORT = os.environ.get('TEMPI_PORT', 5000)
    app.run(HOST, PORT, DEBUG)
