#!/usr/bin/env python3
import time
import threading
import Jetson.GPIO as gpio


class PWM:
    """
    PWM class for software-based PWM control.
    """
    def __init__(self, frequency=100):
        """
        Initializes the SoftwarePWM object.
        Parameters:
            frequency (int): The frequency of the PWM signal.
        """
        self.frequency = frequency
        self.period = 1.0 / self.frequency
        self.current_duty_cycle = 0
        self.running = False
        self.pins = []

    def add_pin(self, pin):
        """
        Adds a pin to the list of pins.
        Parameters:
            pin: The pin to be added.
        Returns:
        None
        """

        self.pins.append(pin)

    def software_pwm(self):
        """
        Implements software PWM (Pulse Width Modulation) for
        controlling the duty cycle of GPIO pins. This method
        continuously runs in a loop while `self.running` is True.
        It calculates the on-time and off-time based on the current
        duty cycle and period. If the on-time is greater than 0, it 
        sets all the pins in `self.pins` to HIGH and sleeps for the
        on-time duration. If the off-time is greater than 0, it sets
        all the pins in `self.pins` to LOW and sleeps for the
        off-time duration.
        Note:
            The duty cycle is represented as a percentage, ranging
            from 0 to 100.
            The period is the total duration of one cycle, in seconds.
        Returns:
            None
        """

        while self.running:
            on_time = self.period * (self.current_duty_cycle / 100.0)
            off_time = self.period - on_time
            if on_time > 0:
                for pin in self.pins:
                    gpio.output(pin, gpio.HIGH)
                time.sleep(on_time)
            if off_time > 0:
                for pin in self.pins:
                    gpio.output(pin, gpio.LOW)
                time.sleep(off_time)

    def start(self, duty_cycle):
        """
        Starts the software PWM with the given duty cycle.
        Parameters:
            duty_cycle (float): The duty cycle of the PWM signal.
        Returns:
            None
        """

        self.current_duty_cycle = duty_cycle
        if not self.running:
            self.running = True
            threading.Thread(target=self.software_pwm, daemon=True).start()

    def stop(self):
        """
        Stops the software PWM.
        This method sets the `running` attribute to False and
        turns off all the pins used for PWM.
        Parameters:
            None
        Returns:
            None
        """

        self.running = False
        for pin in self.pins:
            gpio.output(pin, gpio.LOW)

    def set_duty_cycle(self, duty_cycle):
        """
        Sets the duty cycle for the software PWM.
        Parameters:
            duty_cycle (float): The desired duty cycle value.
            Must be between 0 and 100.
        Returns:
            None
        """

        self.current_duty_cycle = max(0, min(100, duty_cycle))
