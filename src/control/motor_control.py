import Jetson.GPIO as gpio
from time import sleep

# Pin configuration
ena, in1, in2 = 33, 35, 37  

# Board pin numbering scheme
gpio.setmode(gpio.BOARD)
# pins to control rear motors
gpio.setup(ena, gpio.OUT, initial=gpio.HIGH)
gpio.setup(in1, gpio.OUT, initial=gpio.LOW)
gpio.setup(in2, gpio.OUT, initial=gpio.LOW)


# PWM setup (Currently not working...)
# pwm_a = gpio.PWM(ena, 50)  # 100 Hz frequency

def moveForward():
    print("Moving forward")
    gpio.output(in1, gpio.HIGH)
    gpio.output(in2, gpio.LOW)
    # pwm_a.ChangeDutyCycle(10)  # Full speed

def moveBackward():
    print("Moving backward")
    gpio.output(in1, gpio.LOW)
    gpio.output(in2, gpio.HIGH)
    # pwm_a.ChangeDutyCycle(10)  # Full speed

def stopMotors():
    print("Stopping motors")
    gpio.output(ena, gpio.LOW)
    gpio.output(in1, gpio.LOW)
    gpio.output(in2, gpio.LOW)
    # pwm_a.ChangeDutyCycle(0)
    print("Motors stopped")


def main():
    try:
        # pwm_a.start(0)  # Start with 50% duty cycle
        # print("PWM started")

        moveForward()
        sleep(0.5)

        moveBackward()
        sleep(0.5)

        stopMotors()

    except KeyboardInterrupt:
        print("Program stopped by the user")
    finally:
        # pwm_a.stop()
        gpio.cleanup()
        print("Exiting")

if __name__ == "__main__":
    main()