#!/usr/bin/env python
import re
from datetime import datetime
from glob import glob
from os.path import join
from time import sleep

from pitemp import get_config
from pitemp.db import execute

# the base path to the device folder
DEVICE_DIR = '/sys/bus/w1/devices'

args = None


def _read_raw_file():
    """
    Reads the sensor device file and return its contents
    :return:
    """
    global DEVICE_DIR
    sensor_dir = glob(DEVICE_DIR + '/28*')[0]
    sensor_file = join(sensor_dir, 'w1_slave')
    with open(sensor_file, 'r') as fp:
        content = fp.read()
    return list(filter(None, content.split('\n')))


def get_temperature():
    """
    Reads the temperature from the output file
    :return: a tuple consisting of (celsius, fahrenheit)
    """
    lines = _read_raw_file()

    # check we have some data
    if len(lines) != 2 or 'YES' not in lines[0]:
        sleep(0.2)
        lines = _read_raw_file()

    m = re.search(r't=(\d+)', lines[1])
    if not m:
        return

    value = float(m.groups()[0])
    celsius = value / 1000.0
    fahrenheit = celsius * 9.0 / 5.0 + 32.0
    return round(celsius, 2), round(fahrenheit, 2)


def add_reading(celsius, fahrenheit):
    """
    Adds a reading to the database
    :param celsius:
    :param fahrenheit:
    :return:
    """
    sql = 'INSERT INTO `readings` (`location`, `reading_time`, `celsius`, ' \
          '`fahrenheit`) VALUES (%(location)s, %(now)s, %(celsius)s, ' \
          '%(fahrenheit)s)'

    data = {
        'location': get_config('location', 'UNKNOWN'),
        'now': datetime.now(),
        'celsius': celsius,
        'fahrenheit': fahrenheit,
    }

    execute(sql, data)


if __name__ == '__main__':
    while True:
        readings = get_temperature()
        if readings:
            add_reading(*readings)
        sleep(get_config('interval', 60))
