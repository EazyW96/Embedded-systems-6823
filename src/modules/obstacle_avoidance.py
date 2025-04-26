import time
from modules.servo_control import Servo
from modules.sensor_manager import SensorManager

class ObstacleAvoidance:
    def __init__(self, sensor_manager: SensorManager):
        self.sensor = sensor_manager
        self.servo = Servo()
        self.safe_distance = 20  # Safe distance in centimeters

    def scan_environment(self):
        """Scan left, center, and right; return distances."""
        distances = {}

        # Look Left (30 degrees)
        self.servo.set_servo_pwm('0', 30)
        time.sleep(0.2)
        distances['left'] = self.sensor.get_ultrasonic_distance()

        # Look Center (90 degrees)
        self.servo.set_servo_pwm('0', 90)
        time.sleep(0.2)
        distances['center'] = self.sensor.get_ultrasonic_distance()

        # Look Right (150 degrees)
        self.servo.set_servo_pwm('0', 150)
        time.sleep(0.2)
        distances['right'] = self.sensor.get_ultrasonic_distance()

        # Reset to center
        self.servo.set_servo_pwm('0', 90)

        return distances

    def decide_movement(self):
        """Decide movement based on scanned distances."""
        distances = self.scan_environment()
        print(f"[Obstacle Scan] Left: {distances['left']} cm | Center: {distances['center']} cm | Right: {distances['right']} cm")

        # Treat -1 readings as blocked
        if distances['center'] == -1 or distances['left'] == -1 or distances['right'] == -1:
            print("[Warning] Sensor error detected. Treating as obstacle.")
            return "move_backwards"

        if distances['center'] < self.safe_distance:
            if distances['left'] > self.safe_distance:
                return "turn_left"
            elif distances['right'] > self.safe_distance:
                return "turn_right"
            else:
                return "move_backwards"
        else:
            return "move_forward"
