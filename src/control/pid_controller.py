class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute_control(self, target, current):
        error = target - current
        self.integral += error
        derivative = error - self.previous_error
        output = (self.kp * error + self.ki * 
                  self.integral + self.kd * derivative)
        self.previous_error = error
        return output


# Example usage:
if __name__ == "__main__":
    pid = PIDController(1.0, 0.1, 0.01)
    target_speed = 30  # Target speed in km/h
    current_speed = 25  # Current speed in km/h
    control_signal = pid.compute_control(target_speed, current_speed)
    print(f"Control Signal: {control_signal}")
