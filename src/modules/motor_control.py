import time
from modules.pca9685 import PCA9685

class MotorControl:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.set_pwm_freq(50)

    def duty_range(self, duty):
        return max(min(duty, 4095), -4095)

    def set_motor_model(self, duty1, duty2, duty3, duty4):
        # Clamp all duty values
        duty1 = self.duty_range(duty1)
        duty2 = self.duty_range(duty2)
        duty3 = self.duty_range(duty3)
        duty4 = self.duty_range(duty4)

        # Motor 1 (Left Front)
        self._drive_motor(0, 1, duty1)
        # Motor 2 (Left Rear)
        self._drive_motor(2, 3, duty2)
        # Motor 3 (Right Rear)
        self._drive_motor(4, 5, duty4)
        # Motor 4 (Right Front)
        self._drive_motor(6, 7, duty3)

    def _drive_motor(self, pinA, pinB, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(pinA, 0)
            self.pwm.set_motor_pwm(pinB, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(pinB, 0)
            self.pwm.set_motor_pwm(pinA, -duty)
        else:
            self.pwm.set_motor_pwm(pinA, 4095)
            self.pwm.set_motor_pwm(pinB, 4095)

    def move_forward(self, speed=600):
        print("[MOTOR] Moving forward")
        self.set_motor_model(speed, speed, speed, speed)

    def move_backwards(self, speed=600):
        print("[MOTOR] Moving backward")
        self.set_motor_model(-speed, -speed, -speed, -speed)

    def turn_left(self, speed=600):
        print("[MOTOR] Turning left")
        self.set_motor_model(-speed, -speed, speed, speed)

    def turn_right(self, speed=600):
        print("[MOTOR] Turning right")
        self.set_motor_model(speed, speed, -speed, -speed)

    def stop_car(self):
        print("[MOTOR] Stopping car")
        self.set_motor_model(0, 0, 0, 0)
