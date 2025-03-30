from servo_control import Servo
import time

class HeadMovement:
  """
  Class to control head movement using two servo motors (pan & tilt).
  """

  def __init__(self):
    self.servo = Servo()
    self.pan_channel = '0'  # Channel for left-right movement
    self.tilt_channel = '1'  # Channel for up-down movement
    self.current_pan = 90  # Current pan angle (neutral position)
    self.current_tilt = 90  # Current tilt angle (neutral position)
    self.turn_left_right(self.current_pan)
    self.turn_up_down(self.current_tilt)

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
    Sweeps the head side to side.

    Args:
        min_angle (int): Minimum angle for the sweep.
        max_angle (int): Maximum angle for the sweep.
        delay (float): Delay between movements.
    """
    for angle in range(min_angle, max_angle, 10):
      self.turn_left_right(angle)
      time.sleep(delay)
    for angle in range(max_angle, min_angle, -10):
      self.turn_left_right(angle)
      time.sleep(delay)

  def sweep_up_down(self, min_angle=60, max_angle=120, delay=0.5):
    """
    Sweeps the head up and down.

    Args:
        min_angle (int): Minimum angle for the sweep.
        max_angle (int): Maximum angle for the sweep.
        delay (float): Delay between movements.
    """
    for angle in range(min_angle, max_angle, 10):
      self.turn_up_down(angle)
      time.sleep(delay)
    for angle in range(max_angle, min_angle, -10):
      self.turn_up_down(angle)
      time.sleep(delay)

  def turn_left(self, amount):
    """
    Turns the head left by a given amount (decreasing the pan angle).

    Args:
        amount (int): The angle change.
    """
    new_angle = self.current_pan - amount
    if new_angle < 0:
      new_angle = 0
    self.current_pan = new_angle
    self.turn_left_right(self.current_pan)

  def turn_right(self, amount):
    """
    Turns the head right by a given amount (increasing the pan angle).

    Args:
        amount (int): The angle change.
    """
    new_angle = self.current_pan + amount
    if new_angle > 180:
      new_angle = 180
    self.current_pan = new_angle
    self.turn_left_right(self.current_pan)

  def look_up(self, amount):
    """
    Tilts the head upward by a given amount (increasing the tilt angle).

    Args:
        amount (int): The angle change.
    """
    new_angle = self.current_tilt + amount
    if new_angle > 180:
      new_angle = 180
    self.current_tilt = new_angle
    self.turn_up_down(self.current_tilt)

  def look_down(self, amount):
    """
    Tilts the head downward by a given amount (decreasing the tilt angle).

    Args:
        amount (int): The angle change.
    """
    new_angle = self.current_tilt - amount
    if new_angle < 0:
      new_angle = 0
    self.current_tilt = new_angle
    self.turn_up_down(self.current_tilt)


# Testing head movement
# Example
# how to control the head actuator
# basic movements turning left/right, looking up/down,
# and sweeping motions
if __name__ == "__main__":
  head = HeadMovement()

  print("Turning head left by 15 degrees...")
  head.turn_left(15)
  time.sleep(1)

  print("Turning head right by 30 degrees...")
  head.turn_right(30)
  time.sleep(1)

  print("Looking up by 20 degrees...")
  head.look_up(20)
  time.sleep(1)

  print("Looking down by 10 degrees...")
  head.look_down(10)
  time.sleep(1)

  print("Sweeping head left-right...")
  head.sweep_left_right()

  print("Sweeping head up-down...")
  head.sweep_up_down()
