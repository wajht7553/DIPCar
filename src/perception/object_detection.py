#!/usr/bin/python3
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput


class ObjectDetector:
    def __init__(self, model_path, labels_path,
                 threshold=0.5, camera=None,
                 display=False):
        self.model_path = model_path
        self.labels_path = labels_path
        self.threshold = threshold
        self.camera = videoSource(camera)
        if display:
            self.display = videoOutput('display://0')
        self.net = detectNet(
            model=self.model_path, labels=self.labels_path,
            input_blob='input_0', output_cvg='scores',
            output_bbox='boxes', threshold=self.threshold)

    def detect(self):
        while True:
            image = self.camera.Capture()
            detections = self.net.Detect(image)
            for detection in detections:
                print(detection)
            if self.display:
                self.display.Render(image)
                self.display.SetStatus(
                    f"Detection Network {self.net.GetNetworkFPS():.0f} FPS"
                )
            if not self.camera.IsStreaming():
                break


def main():
    model_path = '/home/dipcar/DIPCar/data/models/ssd-mobilenet.onnx'
    labels_path = '/home/dipcar/DIPCar/data/models/labels.txt'
    detector = ObjectDetector(model_path, labels_path, display=True)
    detector.detect()


if __name__ == "__main__":
    main()