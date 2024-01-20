#*************************************************************************************************/
#* Project:   Smart Piggy Bank
#* Subject:   Inzynierski Projekt Zespolowy 2
#* Authors:   Marcel Baranek, Andrzej Miszczuk, Grzegorz Kostanski, Pawel Bieniasz
#* Created:   ZUT - 2023/2024
#*
#* Name:      gpio_tools.py
#* Purpose:   Helper tools for GPIO.
#*************************************************************************************************/

import RPi.GPIO as GPIO
import time
import ST7789
from PIL import Image, ImageDraw, ImageFont
from tools.db_tools import *
from tools.coin_detection_tools import *

SENSOR1_PIN = 4
SENSOR2_PIN = 27
CLEAR_DB_BUTTON_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR1_PIN, GPIO.IN)
GPIO.setup(SENSOR2_PIN, GPIO.IN)
GPIO.setup(CLEAR_DB_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pin1_detected = False
start_time_sensor1 = 0
end_time_sensor1 = 0
start_time_sensor2 = 0
end_time_sensor2 = 0

display = ST7789.ST7789(port=0,cs=1,rst=25,dc=24,backlight=19,
                        spi_speed_hz=160000000, width=240, height=240)
display._spi.mode=3
display.reset()
display._init()
WIDTH = display.width
HEIGHT = display.height

#*************************************************************************************************/
#* Function:  detect_button_callback
#*
#* Purpose:   Callback for clearing databse by holding reset button.
#*************************************************************************************************/
def detect_button_callback(channel):
  if GPIO.input(CLEAR_DB_BUTTON_PIN):
    clear_db()
    print("Database cleared")
    disp_clear_db()

#*************************************************************************************************/
#* Function:  detect_sensor1_callback
#*
#* Purpose:   Callback for detecting coin passing through first sensor.
#*************************************************************************************************/
def detect_sensor1_callback(channel):
  global pin1_detected
  global start_time_sensor1
  global end_time_sensor1

  if not GPIO.input(SENSOR1_PIN):
    start_time_sensor1 = time.time()
    pin1_detected = True
  if GPIO.input(SENSOR1_PIN):
    end_time_sensor1 = time.time()
    elapsed_time = end_time_sensor1 - start_time_sensor1
    print("Sensor 1 - Elapsed time: " + str(elapsed_time))

#*************************************************************************************************/
#* Function:  detect_sensor2_callback
#*
#* Purpose:   Callback for detecting coin passing through second sensor.
#*************************************************************************************************/
def detect_sensor2_callback(channel):
  global pin1_detected
  global end_time_sensor1
  global elapsed_time_sensor2
  global elapsed_time_total
  global coin_passed
  global start_time_sensor2
  global end_time_sensor2

  if not GPIO.input(SENSOR2_PIN) and pin1_detected:
    start_time_sensor2 = time.time()
  if GPIO.input(SENSOR2_PIN) and pin1_detected:
    end_time_sensor2 = time.time()
    elapsed_time_sensor2 = end_time_sensor2 - start_time_sensor2
    elapsed_time_total = start_time_sensor2 - end_time_sensor1
    pin1_detected = False
    print("Elapesed time between sensors: " + str(elapsed_time_total))
    print("Sensor 2 - Elapsed time: " + str(elapsed_time_sensor2))

    disp_inserted_coin(calculate_size(elapsed_time_total, elapsed_time_sensor2))

#*************************************************************************************************/
#* Function:  disp_clear_db
#*
#* Purpose:   Puts the information about clearing the database on the screen.
#*************************************************************************************************/
def disp_clear_db():
  image = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

  draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))

  text1 = "Database"
  text2 = "cleared"

  w1, h1 = draw.textsize(text1, font=font)
  w2, h2 = draw.textsize(text2, font=font)

  x1 = (WIDTH - w1) // 2
  y1 = (HEIGHT - h1) // 2 - h1
  x2 = (WIDTH - w2) // 2
  y2 = (HEIGHT - h2) // 2

  draw.text((x1, y1), text1, font=font, fill=(255, 255, 255))
  draw.text((x2, y2), text2, font=font, fill=(255, 255, 255))

  display.display(image)

  time.sleep(5)
  disp_current_savings()

#*************************************************************************************************/
#* Function:  disp_inserted_coin
#*
#* Purpose:   Updates the screen with the value of inserted coin.
#*************************************************************************************************/
def disp_inserted_coin(coin):
  image = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
  font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

  draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))

  text1 = "Inserted:"
  if coin == 0:
    text2 = "NULL"
  else:
    text2 = "{} zł".format(coin)

  w1, h1 = draw.textsize(text1, font=font)
  w2, h2 = draw.textsize(text2, font=font2)

  x1 = (WIDTH - w1) // 2
  y1 = (HEIGHT - h1) // 2 - h1 - 10  # Subtract 10 to move the text up
  x2 = (WIDTH - w2) // 2
  y2 = (HEIGHT - h2) // 2 + 10  # Add 10 to move the text down

  draw.text((x1, y1), text1, font=font, fill=(255, 255, 255))
  draw.text((x2, y2), text2, font=font2, fill=(255, 255, 255))

  display.display(image)

  time.sleep(5)
  disp_current_savings()

#*************************************************************************************************/
#* Function:  disp_current_savings
#*
#* Purpose:   Updates the screen with value of current savings and coin amounts.
#*************************************************************************************************/
def disp_current_savings():
  savings = round(get_total(), 2)
  coins = get_coins()

  image = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
  font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

  draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))

  w1, h1 = draw.textsize("Savings:", font=font)
  w2, h2 = draw.textsize("{} zł".format(savings), font=font2)
  draw.text(((WIDTH - w1) // 2, 0), "Savings:", font=font, fill=(255, 255, 255))
  draw.text(((WIDTH - w2) // 2, 40), "{} zł".format(savings), font=font2, fill=(255, 255, 255))

  w3, h3 = draw.textsize("----------------------------------", font=font)
  draw.text(((WIDTH - w3) // 2, 90), "----------------------------------", font=font, fill=(255, 255, 255))

  table_structure = [
    ("1gr", coins[0]),
    ("2gr", coins[1]),
    ("5gr", coins[2]),
    ("10gr", coins[3]),
    ("20gr", coins[4]),
    ("50gr", coins[5]),
    ("1zł", coins[6]),
    ("2zł", coins[7]),
    ("5zł", coins[8]),
    ("NULL", coins[9])]

  col_width = WIDTH // 2

  y_text = 120
  for i in range(0, len(table_structure), 2):
    x_text = 0
    for j in range(2):
      if i + j < len(table_structure):
        cell = table_structure[i + j]
        cell_text = "{}: {}".format(cell[0], cell[1])
        w4, h4 = draw.textsize(cell_text, font=font)
        draw.text((x_text + (col_width - w4) // 2, y_text), cell_text, font=font, fill=(255, 255, 255))
        x_text += col_width
    y_text += 20

  display.display(image)

GPIO.add_event_detect(4, GPIO.BOTH, callback=detect_sensor1_callback)
GPIO.add_event_detect(27, GPIO.BOTH, callback=detect_sensor2_callback)
GPIO.add_event_detect(22, GPIO.BOTH, callback=detect_button_callback, bouncetime=5000)

disp_current_savings()
