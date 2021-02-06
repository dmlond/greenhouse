#!/usr/bin/python3

from veml6030 import VEML6030
import smbus2
import qwiic_bme280
import time
import sys

def instrument_metrics(light,temp,humidity):
  metrics_out = open('/home/pi/metrics.prom', 'w+')
  print('# HELP ambient_temperature temperature in fahrenheit', flush=True, file=metrics_out)
  print('# TYPE ambient_temperature gauge', flush=True, file=metrics_out)
  print(f'ambient_temperature {temp}', flush=True, file=metrics_out)
  print('# HELP ambient_light light in lux', flush=True, file=metrics_out)
  print('# TYPE ambient_light gauge', flush=True, file=metrics_out)
  print(f'ambient_light {light}', flush=True, file=metrics_out)
  print('# HELP ambient_humidity humidity in %RH', flush=True, file=metrics_out)
  print('# TYPE ambient_humidity gauge', flush=True, file=metrics_out)
  print(f'ambient_humidity {humidity}', flush=True, file=metrics_out)
  metrics_out.close()

print("Starting Greenhouse Monitor")
bus = smbus2.SMBus(1)  # For Raspberry Pi 
light_sensor = VEML6030(bus)
environment_sensor = qwiic_bme280.QwiicBme280()

if environment_sensor.is_connected() == False:
    print("The Environment Sensor isn't connected to the system. Please check your connection", file=sys.stderr)
    exit(1)
environment_sensor.begin()
while True:
    light = light_sensor.read_light()
    temp = environment_sensor.temperature_fahrenheit
    humidity = environment_sensor.humidity
    instrument_metrics(light, temp, humidity)
    time.sleep(11)
