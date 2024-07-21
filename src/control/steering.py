#!/usr/bin/python3
import time
from adafruit_servokit import ServoKit


class SteeringController:
    """
    A class to control the steering servo of an autonomous
    vehicle prototype using PCA9685 with Jetson Nano.

    This class provides methods to set the steering angle,
    center the steering, and make left or right turns.
    It ensures that the steering angle remains within
    a specified range.

    Attributes:
        kit (ServoKit): ServoKit object for controlling the PCA9685.
        channel (int): The channel number the servo is connected to
        on the PCA9685.
        min_angle (int): The minimum allowed steering angle.
        max_angle (int): The maximum allowed steering angle.
        center_angle (int): The angle corresponding to straight driving
        (default is 90 degrees).
    """

    def __init__(self, channel=0, min_angle=0, max_angle=180):
        """
        Initialize the SteeringController.

        Args:
            channel (int): The channel number the servo is connected to
            (default is 0).
            min_angle (int): The minimum allowed steering angle
            (default is 0).
            max_angle (int): The maximum allowed steering angle
            (default is 180).
        """
        self.kit = ServoKit(channels=16)
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.center_angle = 90

    def set_angle(self, angle):
        """
        Set the steering angle, ensuring it's within the valid range.

        Args:
            angle (int): The desired steering angle.

        Returns:
            None
        """
        clamped_angle = max(self.min_angle, min(self.max_angle, angle))
        self.kit.servo[self.channel].angle = clamped_angle
        print(f"Steering angle set to: {clamped_angle}")

    def center_steering(self):
        """
        Center the steering by setting it to the center angle.

        Returns:
            None
        """
        self.set_angle(self.center_angle)
        print("Steering centered")

    def turn_left(self, degree):
        """
        Turn the steering left by the specified degree.

        Args:
            degree (int): The number of degrees to turn left.

        Returns:
            None
        """
        new_angle = self.center_angle - degree
        self.set_angle(new_angle)

    def turn_right(self, degree):
        """
        Turn the steering right by the specified degree.

        Args:
            degree (int): The number of degrees to turn right.

        Returns:
            None
        """
        new_angle = self.center_angle + degree
        self.set_angle(new_angle)


if __name__ == "__main__":
    # Usage example
    steering = SteeringController(channel=0, min_angle=40, max_angle=130)

    try:
        # Center the steering
        steering.center_steering()
        time.sleep(1)

        # Turn left by 30 degrees
        steering.turn_left(30)
        time.sleep(1)

        # Turn right by 30 degrees
        steering.turn_right(50)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Always center the steering before exiting
        steering.center_steering()
