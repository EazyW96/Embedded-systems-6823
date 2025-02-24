from servo_control import Servo
import time


class HeadMovement:
  """Class to control head movement with two servo motors (pan & tilt)."""

  def __init__(self):
    self.servo = Servo()
    self.pan_channel = '0'  # Channel for left-right movement
    self.tilt_channel = '1'  # Channel for up-down movement

  def turn_left_right(self, angle):
    """
    Moves the head left or right.

    Args:
        angle (int): The angle to set the head (0 to 180 degrees).
    """
    self.servo.set_servo_pwm(self.pan_channel, angle)

  def turn_up_down(self, angle):
    """
    Moves the head up or down.

    Args:
        angle (int): The angle to set the head (0 to 180 degrees).
    """
    self.servo.set_servo_pwm(self.tilt_channel, angle)

  def sweep_left_right(self, min_angle=60, max_angle=120, delay=0.5):
    """
    Moves the head side to side in a sweeping motion.

    Args:
        min_angle (int): Minimum angle for the sweep.
        max_angle (int): Maximum angle for the sweep.
        delay (float): Time delay between movements.
    """
    for angle in range(min_angle, max_angle, 10):
      self.turn_left_right(angle)
      time.sleep(delay)
    for angle in range(max_angle, min_angle, -10):
      self.turn_left_right(angle)
      time.sleep(delay)

  def sweep_up_down(self, min_angle=60, max_angle=120, delay=0.5):
    """
    Moves the head up and down in a sweeping motion.

    Args:
        min_angle (int): Minimum angle for the sweep.
        max_angle (int): Maximum angle for the sweep.
        delay (float): Time delay between movements.
    """
    for angle in range(min_angle, max_angle, 10):
      self.turn_up_down(angle)
      time.sleep(delay)
    for angle in range(max_angle, min_angle, -10):
      self.turn_up_down(angle)
      time.sleep(delay)


# Test head movement
if __name__ == "__main__":
  head = HeadMovement()
  print("Sweeping head left-right...")
  head.sweep_left_right()
  print("Sweeping head up-down...")
  head.sweep_up_down()
