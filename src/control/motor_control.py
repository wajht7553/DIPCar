#!/usr/bin/env python3
import Jetson.GPIO as gpio
import time
import threading

# Board pin numbering scheme
gpio.setmode(gpio.BOARD)

# Pins to control rear motors
ena, in1, in2 = 33, 35, 37
gpio.setup(ena, gpio.OUT, initial=gpio.LOW)
gpio.setup(in1, gpio.OUT, initial=gpio.LOW)
gpio.setup(in2, gpio.OUT, initial=gpio.LOW)

# Software PWM parameters
pwm_frequency = 100  # Hz
pwm_period = 1.0 / pwm_frequency
current_duty_cycle = 0
pwm_running = False


def software_pwm():
    """
    Emulate the PWM
    """
    global pwm_running
    while pwm_running:
        on_time = pwm_period * (current_duty_cycle / 100.0)
        off_time = pwm_period - on_time

        if on_time > 0:
            gpio.output(ena, gpio.HIGH)
            time.sleep(on_time)

        if off_time > 0:
            gpio.output(ena, gpio.LOW)
            time.sleep(off_time)


def start_pwm(duty_cycle):
    """
    Start the PWM with the specified duty cycle
    """
    global current_duty_cycle, pwm_running
    current_duty_cycle = duty_cycle
    if not pwm_running:
        pwm_running = True
        threading.Thread(target=software_pwm, daemon=True).start()


def stop_pwm():
    """
    Stop the PWM
    """
    global pwm_running
    pwm_running = False
    gpio.output(ena, gpio.LOW)


def set_duty_cycle(duty_cycle):
    """
    Change the frequency of the PWM
    """
    global current_duty_cycle
    current_duty_cycle = max(0, min(100, duty_cycle))


def move_forward(speed):
    """
    Move forward with the specified speed
    """
    print(f"Moving forward at {speed}% speed")
    gpio.output(in1, gpio.HIGH)
    gpio.output(in2, gpio.LOW)
    set_duty_cycle(speed)


def move_backward(speed):
    """
    Move back with the specified speed
    """
    print(f"Moving backward at {speed}% speed")
    gpio.output(in1, gpio.LOW)
    gpio.output(in2, gpio.HIGH)
    set_duty_cycle(speed)


def stop_motors():
    """
    Stop the motors
    """
    print("Stopping motors")
    stop_pwm()
    gpio.output(in1, gpio.LOW)
    gpio.output(in2, gpio.LOW)
    print("Motors stopped")


def main():
    try:
        start_pwm(0)  # Start PWM with 0% duty cycle

        move_forward(10)
        time.sleep(5)

        move_forward(50)
        time.sleep(1)

        # move_forward(75)
        # time.sleep(1)

        # move_backward(50)
        # time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by the user")
    finally:
        stop_motors()
        gpio.cleanup()
        print("Exiting")


if __name__ == "__main__":
    main()
