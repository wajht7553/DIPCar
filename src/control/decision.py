#!/usr/bin/python3
class DecisionMaker:
    """
    Class representing a decision maker for a car.
    """

    def __init__(self, car):
        """
        Initializes the Decision class.
        Attributes:
            car: The car object.
            speed: The current speed of the car.
            safe_speed: The safe speed of the car.
            labels: A list of labels for object detection.
            stop_labels: A list of labels indicating a stop.
            caution_labels: A list of labels indicating caution.
            speed_limits: A dictionary mapping speed limit labels
                to their corresponding speeds.
        """

        self.car = car
        self.speed = self.safe_speed = 15
        self.labels = [
            'BACKGROUND', 'bicycle', 'person',
            'speed_limit_120', 'speed_limit_30', 'speed_limit_60',
            'stop', 'traffic_green', 'traffic_red', 'vehicle'
            ]
        self.stop_labels = ['stop', 'traffic_red']
        self.caution_labels = ['person', 'bicycle']
        self.speed_limits = {
            'speed_limit_30': 25,
            'speed_limit_60': 40,
            'speed_limit_120': 50,
        }
        self.start()

    def start(self):
        """
        Starts the decision process for controlling the car.
        This method is responsible for initiating the decision process
        for controlling the car. It calls the 'forward' method of the
        'car' object with the safe speed.
        Parameters:
            self: The instance of the 'decision' class.
        Returns:
            None
        """

        self.car.forward(self.safe_speed)

    def make_decision(self, detections):
        """
        Makes a decision based on the given detections.
        Parameters:
            detections: A list of detections.
        Returns:
            None
        """
        self.car.is_moving = True
        is_cautious = False
        for detection in detections:
            label_id = detection.ClassID
            label = self.labels[label_id]

            if label in self.stop_labels:
                self.car.stop()
                print('Stop sign detected. Stopping the car.')
                return
            elif label in self.caution_labels:
                is_cautious = True
                self.car.is_moving = True
                print(f'{label} detected. Slowing down.')
            elif label in self.speed_limits:
                self.speed = self.speed_limits[label]
                self.car.is_moving = True
                print(f'Speed limit {self.speed} detected. Adjusting speed.')
            else:
                self.car.is_moving = True

        if not self.car.is_moving:
            return
        elif is_cautious:
            self.car.forward(self.safe_speed)
        else:
            self.car.forward(self.speed)
