#!/usr/bin/env python3
import time
import threading
import Jetson.GPIO as gpio


class PWM:
    """
    Software based Pulse Width Modulation (PWM)
    """    
    def __init__(self, frequency=100):
        """
        Initialize the PWM properties

        Args:
            frequency (int, optional): frequency of the PWM. Defaults to 100.
        """        
        self.frequency = frequency
        self.period = 1.0 / self.frequency
        self.current_duty_cycle = 0
        self.running = False
        self.pins = []

    def add_pin(self, pin):
        """
        Add pin to enable PWM on that

        Args:
            pin (GPIO pin channel): Pin number
        """        
        self.pins.append(pin)

    def software_pwm(self):
        """
        Emulate PWM on a given pin(s)
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
        Start software based PWM on its own thread

        Args:
            duty_cycle (int): duty cycle of the PWM
        """        
        self.current_duty_cycle = duty_cycle
        if not self.running:
            self.running = True
            threading.Thread(target=self.software_pwm, daemon=True).start()

    def stop(self):
        """
        Stop software based PWM
        """        
        self.running = False
        for pin in self.pins:
            gpio.output(pin, gpio.LOW)

    def set_duty_cycle(self, duty_cycle):
        """
        Change the duty cycle to the specified value

        Args:
            duty_cycle (int): duty cycle of the PWM
        """        
        self.current_duty_cycle = max(0, min(100, duty_cycle))
