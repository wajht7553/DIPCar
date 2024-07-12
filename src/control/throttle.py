#!/usr/bin/env python3
import Jetson.GPIO as GPIO
import time
import threading


class ThrottleController:
    """
    A class to control throttle using software PWM on a Jetson Nano.
    """
    def __init__(self, ena_pin, in1_pin, in2_pin, pwm_frequency=100):
        """
        Initialize the ThrottleController.

        :param ena_pin: The enable pin number
        :param in1_pin: The first input pin number
        :param in2_pin: The second input pin number
        :param pwm_frequency: PWM frequency in Hz, defaults to 100
        """
        GPIO.setmode(GPIO.BOARD)
        self.ena_pin = ena_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.pwm_frequency = pwm_frequency
        self.pwm_period = 1.0 / pwm_frequency
        self.current_duty_cycle = 0
        self.pwm_running = False

        GPIO.setup(self.ena_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in1_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in2_pin, GPIO.OUT, initial=GPIO.LOW)

    def _software_pwm(self):
        """
        Internal method to generate software PWM signal.
        This method runs in a separate thread.
        """
        while self.pwm_running:
            on_time = self.pwm_period * (self.current_duty_cycle / 100.0)
            off_time = self.pwm_period - on_time

            if on_time > 0:
                GPIO.output(self.ena_pin, GPIO.HIGH)
                time.sleep(on_time)

            if off_time > 0:
                GPIO.output(self.ena_pin, GPIO.LOW)
                time.sleep(off_time)

    def start_pwm(self):
        """
        Start the PWM signal generation.
        """
        if not self.pwm_running:
            self.pwm_running = True
            threading.Thread(target=self._software_pwm, daemon=True).start()

    def stop_pwm(self):
        """
        Stop the PWM signal generation and set the enable pin to LOW.
        """
        self.pwm_running = False
        GPIO.output(self.ena_pin, GPIO.LOW)

    def set_throttle(self, percentage):
        """
        Set the throttle to a specific percentage.

        :param percentage: Throttle percentage (0-100)
        """
        self.current_duty_cycle = max(0, min(100, percentage))
        if not self.pwm_running:
            self.start_pwm()

    def forward(self, speed):
        """
        Set the motor to move forward at the specified speed.

        :param speed: Forward speed percentage (0-100)
        """
        print("Moving forward at {}% speed".format(speed))
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.set_throttle(speed)

    def reverse(self, speed):
        """
        Set the motor to move in reverse at the specified speed.

        :param speed: Reverse speed percentage (0-100)
        """
        print("Moving backward at {}% speed".format(speed))
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        self.set_throttle(speed)

    def stop(self):
        """
        Set the motor to move forward at the specified speed.

        :param speed: Forward speed percentage (0-100)
        """
        print("Stopping motors")
        self.stop_pwm()
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        print("Motors stopped")

    def cleanup(self):
        """
        Stop the motor, PWM signal, and clean up GPIO resources.
        """
        self.stop()
        GPIO.cleanup()


def main():
    throttle = ThrottleController(ena_pin=33, in1_pin=35, in2_pin=37)

    try:
        throttle.forward(25)
        time.sleep(1)

        throttle.forward(50)
        time.sleep(1)

        throttle.forward(75)
        time.sleep(1)

        throttle.reverse(50)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by the user")
    finally:
        throttle.cleanup()
        print("Exiting")


if __name__ == "__main__":
    main()
