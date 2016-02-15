PiTemp
------

A project that logs data from the temperature sensor and visualises it in the
web browser. I've created this app to work with the tutorial from [CamJam](http://camjam.me/?page_id=623).

![Screenshot](/static/screenshot.png?raw=true)


### Installation

You will need the Python development headers to build the MySQL client library.

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python-dev
    
Install MySQL and create a new database

    sudo apt-get install mysql-server mysql-client
    
Execute the database script on your new database

    mysql -u [username] -p [password] [database] < database.sql
    
Install the app dependencies

    pip install -r requirements.txt
    bower install

Create the config file and edit its contents so that your app can connect to
the database.

    cp config.json-sample config.json
    
### Start logging the temperature

This script will use the values in the `config.json` to connect to the database
and log events.

    PYTHONPATH=`pwd` python pitemp/logger.py &
    
(This will run the logger in the background)
    
### Start the web application

    ./runserver.sh
    
You can now visit the page in your browser by using the RPi's IP address e.g.

    http://192.168.0.9:5000
