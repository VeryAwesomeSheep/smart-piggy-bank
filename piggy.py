#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      piggy.py
#* Purpose:   Flask server, the main brains of the project. Handles coin detection, database
#             operations and web interface and physical display.
#*************************************************************************************************/

#run from home dir with "flask --app piggy run --debug --host=0.0.0.0 --port=7001"

from flask import Flask, url_for, redirect, render_template, request
import json, sqlite3
from tools.db_tools import *
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(27, GPIO.IN)

start_sensor1 = 0
end_sensor1 = 0
start_sensor2 = 0
end_sensor2 = 0

def detect_sensor1_callback(channel):
    global start_sensor1
    global end_sensor1
    if not GPIO.input(4):
        start_sensor1 = time.time()
    if GPIO.input(4):
        end_sensor1 = time.time()
        elapsed = end_sensor1 - start_sensor1
        print("Sensor 1 - Elapsed time: " + str(elapsed))

def detect_sensor2_callback(channel):
    global start_sensor1
    global start_sensor2
    global end_sensor2
    if not GPIO.input(27):
        start_sensor2 = time.time()
    if GPIO.input(27):
        end_sensor2 = time.time()
        elapsed = end_sensor2 - start_sensor2
        elapsed_between = start_sensor2 - start_sensor1
        print("Elapesed time between sensors: " + str(elapsed_between))
        print("Sensor 2 - Elapsed time: " + str(elapsed))

GPIO.add_event_detect(4, GPIO.BOTH, callback=detect_sensor1_callback)
GPIO.add_event_detect(27, GPIO.BOTH, callback=detect_sensor2_callback)

@app.route('/')
def index():
  create_db()

  data_coins = get_coins()
  data_dates, data_values = get_total_from_dates()
  data_table = get_all()

  return render_template('index.html', data_dates=data_dates,
                         data_values=data_values, data_coins=data_coins, data_table=data_table)