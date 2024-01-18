#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      piggy.py
#* Purpose:   Flask server, the main brains of the project. Handles coin detection, database
#             operations, web interface and physical display.
#*************************************************************************************************/

from flask import Flask, url_for, redirect, render_template, request

from tools.db_tools import *
from tools.gpio_tools import *

app = Flask(__name__)

@app.route('/')
def index():
  create_db()

  data_coins = get_coins()
  data_dates, data_values = get_total_from_dates()
  data_table = get_all()

  return render_template('index.html', data_dates=data_dates,
                         data_values=data_values, data_coins=data_coins, data_table=data_table)

if __name__ == "__main__":
  app.run(debug=False, host='0.0.0.0', port=7001)
