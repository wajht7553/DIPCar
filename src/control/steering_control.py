from gpiozero import Motor, OutputDevice


class SteeringControl:
    def __init__(self, motor_pins, enable_pin):
        self.motor = Motor(forward=motor_pins[0], backward=motor_pins[1])
        self.enable = OutputDevice(enable_pin)
        self.enable.on()

    def steer(self, direction, speed=1.0):
        if direction == "left":
            self.motor.backward(speed)
        elif direction == "right":
            self.motor.forward(speed)
        else:
            self.motor.stop()

    def stop(self):
        self.motor.stop()
        self.enable.off()


# Example usage:
if __name__ == "__main__":
    steering_motor = SteeringControl(motor_pins=(27, 22), enable_pin=17)
    steering_motor.steer("left", 0.5)
    steering_motor.stop()
