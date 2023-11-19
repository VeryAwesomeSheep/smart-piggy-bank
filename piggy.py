#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      piggy.py
#* Purpose:   Flask server. Responsible for handling database and displaying data.
#*************************************************************************************************/

#run from home dir with "flask --app server run --debug --host=0.0.0.0 --port=7001"

from flask import Flask, url_for, redirect, render_template, request
import json, sqlite3
from tools.db_tools import *

app = Flask(__name__)

@app.route('/')
def index():
  create_db()

  data_coins = get_coins()
  data_dates, data_values = get_total_from_dates()
  data_table = get_all()

  return render_template('index.html', data_dates=data_dates,
                         data_values=data_values, data_coins=data_coins, data_table=data_table)