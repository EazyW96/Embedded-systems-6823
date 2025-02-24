"""
Main entry point for the Autonomous Navigation System.

This file initializes all necessary modules, loads configuration parameters,
and starts the main control loop for the robot.
"""

from modules.head_movement import HeadMovement


def main():
  head = HeadMovement()

  print("Sweeping head left-right...")
  head.sweep_left_right()

  print("Sweeping head up-down...")
  head.sweep_up_down()


if __name__ == "__main__":
  main()
