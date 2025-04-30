from modules.servo_control import Servo
import time

class HeadMovement:
    """
    Class to control head movement using two servo motors (pan & tilt).
    """
    def __init__(self):
        self.servo = Servo()
        self.pan_channel = '0'  # Channel for left-right movement
        self.tilt_channel = '1'  # Channel for up-down movement
        self.current_pan = 55  # Current pan angle (neutral position)
        self.current_tilt = 90  # Current tilt angle (neutral position)
        self.turn_left_right(self.current_pan)
        self.turn_up_down(self.current_tilt)

    def turn_left_right(self, angle):
        self.servo.set_servo_pwm(self.pan_channel, angle)

    def turn_up_down(self, angle):
        self.servo.set_servo_pwm(self.tilt_channel, angle)

# Testing head movement
if __name__ == "__main__":
    head = HeadMovement()
    #print("Turning head left by 15 degrees...")
    #head.turn_left(15)
    #time.sleep(1)
    #print("Turning head right by 30 degrees...")
    #head.turn_right(30)
    #time.sleep(1)
    #print("Looking up by 20 degrees...")
    #head.look_up(20)
    #time.sleep(1)
    #print("Looking down by 10 degrees...")
    #head.look_down(10)
    #time.sleep(1)
    #print("Sweeping head left-right...")
    #head.sweep_left_right()
    #print("Sweeping head up-down...")
    #head.sweep_up_down()
