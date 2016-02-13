import argparse
from glob import glob
from os.path import join, abspath, dirname

# the argparse module gives us a nice command line interface to gather user
# options
parser = argparse.ArgumentParser(description='Temperature sensor logger')
parser.add_argument('-i', '--interval', type=int, default=60,
                    help='Number of seconds to poll the sensor for new data')

# the base path to the device folder
DEVICE_DIR = '/sys/bus/w1/devices'

# the sensor for the 1 wire device will start with 28, so we use the glob
# module to search for the full name.
SENSOR_DIR = glob(DEVICE_DIR + '/28*')[0]

# this is the file that contains the sensor data that we will parse
SENSOR_FILE = join(SENSOR_DIR, 'w1_slave')

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
