import Jetson.GPIO as GPIO
import time

# Pin Definitions
pwm_pin = 33  # PWM pin connected to an LED

# Constants
PWM_FREQ = 100  # 1 kHz frequency

def setup_pwm():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm_pin, GPIO.OUT, initial=GPIO.LOW)
    pwm = GPIO.PWM(pwm_pin, PWM_FREQ)
    return pwm

def test_pwm(pwm):
    try:
        # Start PWM with 0% duty cycle
        pwm.start(0)
        print("Starting PWM test. Press Ctrl+C to exit.")
        
        # Ramp up duty cycle from 0 to 100% in steps
        for duty_cycle in range(0, 101, 10):
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"Duty Cycle: {duty_cycle}%")
            time.sleep(2)
        
        # Ramp down duty cycle from 100 to 0% in steps
        for duty_cycle in range(100, -1, -10):
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"Duty Cycle: {duty_cycle}%")
            time.sleep(2)

    except KeyboardInterrupt:
        print("PWM test interrupted.")

    finally:
        pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")

def main():
    pwm = setup_pwm()
    test_pwm(pwm)

if __name__ == '__main__':
    main()
