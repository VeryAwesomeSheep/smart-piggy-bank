import RPi.GPIO as GPIO
import time

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

while True:
    time.sleep(0.001)