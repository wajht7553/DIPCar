#!/usr/bin/python3
import time
import Jetson.GPIO as gpio
from src.control.software_pwm import PWM


class DIPCar:
    """
    DIPCar, composed of left and right motors that control the
    longitudnal as well as the lateral movement of the car.
    A simple prototype model, indeed.
    """
    def __init__(self,
                 left_motor_pins=(31, 32, 33),
                 right_motor_pins=(36, 37, 38)
                 ):
        """
        Initializes the motor controller object.
        Args:
            left_motor_pins (tuple): A tuple containing the GPIO pins
                for the left motor.
            right_motor_pins (tuple): A tuple containing the GPIO pins
                for the right motor.
        """
        gpio.setmode(gpio.BOARD)
        self.ena, self.in1, self.in2 = left_motor_pins
        self.enb, self.in3, self.in4 = right_motor_pins
        self.setup_pins()

        self.pwm = PWM()
        self.pwm.add_pin(self.ena)
        self.pwm.add_pin(self.enb)
        self.pwm.start(0)

        self.is_moving = False

    def setup_pins(self):
        """
        Sets up the GPIO pins for motor control.
        This method initializes the GPIO pins for motor control by
        setting them as outputs and setting their initial state to LOW.

        Args:
            None
        Returns:
            None
        """
        for pin in [self.ena, self.in1, self.in2,
                    self.enb, self.in3, self.in4]:
            gpio.setup(pin, gpio.OUT, initial=gpio.LOW)

    def forward(self, speed):
        """
        Moves the car forward at the specified speed.
        Args:
            speed (int): The speed of the motors, ranging from 0 to 100.
        Returns:
            None
        """

        print(f"Moving forward at {speed}% speed")
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.HIGH)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.pwm.set_duty_cycle(speed)
        self.is_moving = True

    def backward(self, speed):
        """
        Moves the car backward at the specified speed.
        Args:
            speed (int): The speed of the motors, ranging from 0 to 100.
        Returns:
            None
        """
        print(f"Moving backward at {speed}% speed")
        gpio.output(self.in1, gpio.HIGH)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.HIGH)
        gpio.output(self.in4, gpio.LOW)
        self.pwm.set_duty_cycle(speed)
        self.is_moving = True

    def steer_left(self, speed, turn_factor=0.5):
        """
        Steers the car to the left at a specified speed.

        Args:
            speed (int): The speed at which to turn left,
                expressed as a percentage.
            turn_factor (float): The factor by which to reduce the speed
                of the right motor. Default is 0.5.
        Returns:
            None
        """
        print(f"Turning left at {speed}% speed")
        # left_speed = speed * (1 - turn_factor)
        right_speed = speed

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.pwm.start(right_speed)
        self.is_moving = True

    def steer_right(self, speed, turn_factor=0.5):
        """
        Steers the car to the right at a specified speed.

        Args:
            speed (int): The speed at which to turn right,
                expressed as a percentage.
            turn_factor (float): The factor by which to reduce the speed
                of the left motor. Default is 0.5.
        Returns:
            None
        """
        print(f"Turning right at {speed}% speed")
        left_speed = speed
        # right_speed = speed * (1 - turn_factor)
        # right_speed = 0

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.HIGH)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)
        self.pwm.start(left_speed)
        self.is_moving = True

    def stop(self):
        """
        Stops the motors.
        This method stops the motors by setting the GPIO pins to LOW.

        Args:
            None
        Returns:
            None
        """

        for pin in [self.in1, self.in2, self.in3, self.in4]:
            gpio.output(pin, gpio.LOW)
        self.is_moving = False
        print("Motors stopped")

    def cleanup(self):
        """
        Clean up the motor controller by stopping the motors,
        pwm and cleaning up GPIO resources.

        Args:
            None
        Returns:
            None
        """

        self.stop()
        self.pwm.stop()
        gpio.cleanup()


def main():
    print("DIPCar started...")
    dipcar = DIPCar()

    while True:
        try:
            dipcar.forward(25)
            time.sleep(2)

            dipcar.steer_left(35)
            time.sleep(2)

            dipcar.steer_right(25)
            time.sleep(2)

            dipcar.backward(25)
            time.sleep(2)

        except KeyboardInterrupt:
            print("Program stopped by the user")
            dipcar.cleanup()
            break

if __name__ == "__main__":
    main()