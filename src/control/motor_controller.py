#!/usr/bin/env python3
import time
from software_pwm import PWM
import Jetson.GPIO as gpio


class DIPCar:
    """
    DIPCar, composed of left and right motors that control the longitudnal
    as well as the lateral movement of the car. A very simple prototype model,
    indeed.
    """    
    def __init__(self,
                 left_motor_pins=(31, 32, 33),
                 right_motor_pins=(36, 37, 38)
                 ):
        """
        Initialize and setup the pins to which the motors are connected
        """        
        gpio.setmode(gpio.BOARD)
        self.ena, self.in1, self.in2 = left_motor_pins
        self.enb, self.in3, self.in4 = right_motor_pins

        self._setup_pins()

        self.pwm = PWM()
        self.pwm.add_pin(self.ena)
        self.pwm.add_pin(self.enb)

    def _setup_pins(self):
        """
        Setup the pins as output pins starting with LOW values
        """        
        for pin in [self.ena, self.in1, self.in2,
                    self.enb, self.in3, self.in4]:
            gpio.setup(pin, gpio.OUT, initial=gpio.LOW)

    def forward(self, speed):
        """
        Move DIPCar forward at specified speed

        Args:
            speed (int): forward speed
        """        
        print(f"Moving forward at {speed}% speed")
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.HIGH)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.pwm.set_duty_cycle(speed)

    def backward(self, speed):
        """
        Move DIPCar backward at specified speed

        Args:
            speed (int): backward speed
        """        
        print(f"Moving backward at {speed}% speed")
        gpio.output(self.in1, gpio.HIGH)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.HIGH)
        gpio.output(self.in4, gpio.LOW)
        self.pwm.set_duty_cycle(speed)

    def steer_left(self, speed, turn_factor=0.5):
        """
        Steer DIPCar to the left

        Args:
            speed (int): turn speed
            turn_factor (float, optional): turn speed will be reduced by
                                           this factor. Defaults to 0.5.
        """        
        print(f"Turning left at {speed}% speed")
        # left_speed = speed * (1 - turn_factor)
        right_speed = speed

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.pwm.start(right_speed)

    def steer_right(self, speed, turn_factor=0.5):
        """
        Steer DIPCar to the right

        Args:
            speed (int): turn speed
            turn_factor (float, optional): turn speed will be reduced by
                                           this factor. Defaults to 0.5.
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

    def stop_motors(self):
        """
        Stop DIPCar
        """        
        print("Stopping motors")
        self.pwm.stop()
        for pin in [self.in1, self.in2, self.in3, self.in4]:
            gpio.output(pin, gpio.LOW)
        print("Motors stopped")

    def cleanup(self):
        """
        Perform necessary cleanup after stopping DIPCar
        """        
        self.stop_motors()
        gpio.cleanup()
        print("Exiting")


def main():
    """
    Test DIPCar
    """    
    print("DIPCar started...")
    dipcar = DIPCar()
    dipcar.pwm.start(0)  # Start PWM with 0% duty cycle
    
    while True:
        try:
            # dipcar.forward(25)
            # time.sleep(2)

            dipcar.steer_left(35)
            time.sleep(2)

            # dipcar.steer_right(25)
            # time.sleep(2)

            # dipcar.backward(25)
            # time.sleep(5)

        except KeyboardInterrupt:
            print("Program stopped by the user")
            dipcar.cleanup()
            break

if __name__ == "__main__":
    main()