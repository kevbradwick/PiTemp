#!/usr/bin/env python
import argparse
import re
from time import sleep
from glob import glob
from os.path import join


# the argparse module gives us a nice command line interface to gather user
# options
parser = argparse.ArgumentParser(description='Temperature sensor logger')
parser.add_argument('-i', type=int, default=60, metavar='SECONDS',
                    help='Number of seconds to poll the sensor for new data')
parser.add_argument('-s', metavar='HOST', default='localhost', help='MySQL host')
parser.add_argument('-u', metavar='USER', default='root', help='MySQL username')
parser.add_argument('-p', metavar='PASSWORD', default='', help='MySQL password')
parser.add_argument('-d', metavar='DB', default='tempi', help='MySQL database')
parser.add_argument('-l', metavar='LOCATION', help='The location of the sensor',
                    default='UNKNOWN')

# the base path to the device folder
DEVICE_DIR = '/sys/bus/w1/devices'


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


def _read_temperature():
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
    return celsius, fahrenheit


if __name__ == '__main__':
    args = parser.parse_args()
    while True:
        print(_read_temperature())
        sleep(args.i)
