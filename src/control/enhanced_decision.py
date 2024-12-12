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
        self.detections = []
        self.segmentation = None
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
            'speed_limit_60': 50,
            'speed_limit_120': 70,
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

    def update_detections(self, detections):
        """
        Updates the detections.
        Parameters:
            detections: A list of detections.
        Returns:
            None
        """

        self.detections = detections

    def update_segmentation(self, segmentation):
        """
        Updates the segmentation.
        Parameters:
            segmentation: The segmentation.
        Returns:
            None
        """

        self.segmentation = segmentation

    def make_decision(self):
        """
        Makes a decision based on the given detections.
        Parameters:
            None
        Returns:
            None
        """

        self._process_detections()
        self._process_segmentation()
        self._control_car()

    def _process_detections(self):
        pass

    def _process_segmentation(self):
        pass

    def _control_car(self):
        pass
