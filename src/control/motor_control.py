from gpiozero import Motor, OutputDevice
from time import sleep


class MotorControl:
    def __init__(self, motor_pins, enable_pin):
        self.motor = Motor(forward=motor_pins[0], backward=motor_pins[1])
        self.enable = OutputDevice(enable_pin)
        self.enable.on()

    def set_speed(self, speed):
        if speed > 0:
            self.motor.forward(speed)
        elif speed < 0:
            self.motor.backward(-speed)
        else:
            self.motor.stop()

    def stop(self):
        self.motor.stop()
        self.enable.off()


# Example usage:
if __name__ == "__main__":
    rear_motor = MotorControl(motor_pins=(13, 15), enable_pin=11)
    rear_motor.set_speed(1)
    sleep(2)
    rear_motor.stop()
