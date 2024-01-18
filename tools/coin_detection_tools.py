#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      coin_detection_tools.py
#* Purpose:   Helper tools for coin detection.
#*************************************************************************************************/

from tools.gpio_tools import *
from tools.db_tools import *

#*************************************************************************************************/
#* Const table:  COINS_PARAMS_TABLE
#*
#* Purpose:     Holds coins data. Each coin denomination has assigned speed [min, max]
#*              and diameter [min, max].
#*************************************************************************************************/
COINS_PARAMS_TABLE = {#0.01: [0, 0],
                      #0.02: [0, 0],
                      #0.05: [0, 0],
                      0.1: [[65, 85], [2.5, 3.0]],
                      0.2: [[62, 95], [3.15, 3.70]],
                      0.5: [[88, 103], [3.85, 4.45]],
                      #1.0: [0, 0],
                      2.0: [[65, 85], [4.18, 4.55]],
                      5.0: [[85, 115], [5.1, 5.8]],}

#*************************************************************************************************/
#* Function:  calculate_size
#*
#* Purpose:   Calculates size based on time measurements and inserts coin into database.
#*************************************************************************************************/
def calculate_size(time_between_sensors, time_sensor2):
  calculated_speed = 2 / time_between_sensors # 2cm is distance between sensors
  calculated_diameter = time_sensor2 * calculated_speed

  print("Calculated speed:", calculated_speed)
  print("Calculated diameter:", calculated_diameter, "\n")

  for coin, params in COINS_PARAMS_TABLE.items():
    if calculated_speed >= params[0][0] and calculated_speed <= params[0][1] and calculated_diameter >= params[1][0] and calculated_diameter <= params[1][1]:
      print("Detected coin:", coin, "\n")
      insert_coin(coin)
      return coin

  print("No coin detected.\n")
  insert_coin(0)
  return 0
