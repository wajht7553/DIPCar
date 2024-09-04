#!/usr/bin/python3


class DecisionMaker:
    def __init__(self, car):
        self.car = car
        self.speed = self.safe_speed = 25
        self.labels = [
            'BACKGROUND', 'bicycle', 'bus', 'car', 'motorcycle', 'person', 
            'speed_limit_120', 'speed_limit_30', 'speed_limit_60',
            'stop', 'traffic_green', 'traffic_red','traffic_yellow'
            ]
        self.stop_labels = ['stop', 'traffic_red']
        self.cation_labels = ['person', 'bicycle',]
        self.speed_limits = {
            'speed_limit_30': 30,
            'speed_limit_60': 60,
            'speed_limit_120': 90,
        }
        self.start()

    def start(self):
        self.car.forward(self.safe_speed)

    def make_decision(self, detections):
        is_cautious = False
        self.car.is_moving = True
        for detection in detections:
            label_id = detection.ClassID
            label = self.labels[label_id]

            if label in self.stop_labels:
                self.car.stop()
                print('Stop sign detected. Stopping the car.')
                return
            elif label in self.cation_labels:
                is_cautious = True
                print(f'{label} detected. Slowing down.')
            elif label in self.speed_limits:
                self.speed = self.speed_limits[label]
                print(f'Speed limit {self.speed} detected. Adjusting speed.')
        if not self.car.is_moving:
            return
        elif is_cautious:
            self.car.forward(self.safe_speed)
        else:
            self.car.forward(self.speed)
