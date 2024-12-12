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