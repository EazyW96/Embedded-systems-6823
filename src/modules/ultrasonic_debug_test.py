
# Simple Ultrasonic Sensor Debug Test
# Make sure you connect TRIG and ECHO correctly and VCC is 5V!

import RPi.GPIO as GPIO
import time

# GPIO Mode (BCM)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
GPIO_TRIGGER = 23  # Change to your actual TRIG pin
GPIO_ECHO = 24     # Change to your actual ECHO pin

# Set GPIO direction
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # Trigger pulse
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Wait for echo start
    start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Wait for echo end
    stop_time = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate distance
    elapsed_time = stop_time - start_time
    dist = (elapsed_time * 34300) / 2
    return dist

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print(f"Measured Distance = {dist:.2f} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()
