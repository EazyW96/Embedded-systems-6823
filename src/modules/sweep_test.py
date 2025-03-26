import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.servo_control import Servo
import time

servo = Servo()

try:
    while True:
        for angle in range(60, 120, 10):  # Sweep one way
            servo.set_servo_pwm('0', angle)
            time.sleep(0.3)

        for angle in range(120, 60, -10):  # Sweep back
            servo.set_servo_pwm('0', angle)
            time.sleep(0.3)

except KeyboardInterrupt:
    print("Sweep ended.")

