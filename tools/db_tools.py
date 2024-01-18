#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      db_tools.py
#* Purpose:   Helper tools for database operations.
#*************************************************************************************************/

import sqlite3, json
from datetime import datetime

#*************************************************************************************************/
#* Function:  create_db
#*
#* Purpose:   Creates database if not exists.
#*************************************************************************************************/
def create_db():
  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS coins
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   time TEXT,
                   coin REAL,
                   total REAL)''')
    con.commit()

#*************************************************************************************************/
#* Function:  get_all
#*
#* param[out] data - list of dictionaries with all records from database
#*
#* Purpose:   Fetches all records from database.
#*************************************************************************************************/
def get_all():
  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('SELECT * FROM coins')
    output = cur.fetchall()

  data = []
  for row in output:
    data.append({
      'id': row[0],
      'date': row[1],
      'time': row[2],
      'coin': row[3],
      'total': row[4],
    })

  return data

#*************************************************************************************************/
#* Function:  insert_coin
#*
#* @param[in] coin - coin value
#*
#* Purpose:   Inserts new record to database.
#*************************************************************************************************/
def insert_coin(coin):
  create_db()

  record = [datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), coin, round(get_total() + coin, 2)]

  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('INSERT INTO coins VALUES (NULL,?,?,?,?)', record)
    con.commit()

#*************************************************************************************************/
#* Function:  get_coins
#*
#* @param[out] coin_amounts - list of coins amounts
#*
#* Purpose:   Fetches coins amounts from database.
#*************************************************************************************************/
def get_coins():
  coin_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  coin_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 0]

  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('SELECT coin, COUNT(*) FROM coins GROUP BY coin')
    output = cur.fetchall()

  for coin, count in output:
    if coin in coin_values:
      coin_amounts[coin_values.index(coin)] = count

  return coin_amounts

#*************************************************************************************************/
#* Function:  get_total_from_dates
#*
#* @param[out] data_dates - list of dates
#* @param[out] data_values - list of total values
#*
#* Purpose:   Fetches dates and max sum from days from database.
#*************************************************************************************************/
def get_total_from_dates():
  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('SELECT date, MAX(total) FROM coins GROUP BY date')
    output = cur.fetchall()

  output.sort(key=lambda x: datetime.strptime(x[0], '%d.%m.%Y'))

  data_dates = []
  data_values = []

  for i in range(len(output)):
    data_dates.append(output[i][0])
    data_values.append(output[i][1])

  return data_dates, data_values

#*************************************************************************************************/
#* Function:  get_total
#*
#* @param[out] output - total sum of coins
#*
#* Purpose:   Fetches total sum of coins from database.
#*************************************************************************************************/
def get_total():
  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('SELECT SUM(coin) FROM coins')
    output = cur.fetchone()

  return 0 if output[0] is None else output[0]

#*************************************************************************************************/
#* Function:  clear_db
#*
#* Purpose:   Clears database.
#*************************************************************************************************/
def clear_db():
  with sqlite3.connect('piggy.db') as con:
    cur = con.cursor()
    cur.execute('DELETE FROM coins')
    con.commit()
