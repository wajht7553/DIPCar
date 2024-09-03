from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput


class DetectNet(detectNet):
    def __init__(self, model_path, labels_path,
                 threshold=0.5, camera=None, display=False):
        super().__init__(
            model=model_path, labels=labels_path, input_blob='input_0',
            output_cvg='scores', output_bbox='boxes', threshold=threshold
        )
        self.camera = videoSource(camera) if camera else None
        self.display = videoOutput('display://0') if display else None

    def detect(self):
        while self.camera and self.camera.IsStreaming():
            image = self.camera.Capture()
            detections = self.Detect(image)

            if self.display:
                self.display.Render(image)
                self.display.SetStatus(
                    f"Detection Network {self.GetNetworkFPS():.0f} FPS")

            yield detections

def main():
    model_path = '/home/dipcar/DIPCar/data/models/ssd-mobilenet.onnx'
    labels_path = '/home/dipcar/DIPCar/data/models/labels.txt'
    detector = DetectNet(
        model_path, labels_path,
        camera="/dev/video0", display=True
    )

    for detections in detector.detect_loop():
        # Process detections here
        print(detections)


if __name__ == "__main__":
    main()


# #!/usr/bin/python3
# from jetson_inference import detectNet
# from jetson_utils import videoSource, videoOutput


# class ObjectDetector():
#     """
#     Class for performing object detection using a custom trained model.
#     Args:
#         model_path (str): The path to the model file.
#         labels_path (str): The path to the labels file.
#         threshold (float, optional): The detection threshold.
#         Defaults to 0.5.
#         camera (str, optional): The camera source. Defaults to None.
#         display (bool, optional): Whether to display the detection
#         results. Defaults to False.
#     """

#     def __init__(self, model_path, labels_path,
#                  threshold=0.5, camera=None,
#                  display=False):
#         """
#         Initializes an object detection instance.
#         Args:
#             model_path (str): The path to the model file.
#             labels_path (str): The path to the labels file.
#             threshold (float, optional): The detection threshold.
#             Defaults to 0.5.
#             camera (str, optional): The camera source. Defaults to None.
#             display (bool, optional): Whether to display the output.
#             Defaults to False.
#         """
#         self.model_path = model_path
#         self.labels_path = labels_path
#         self.threshold = threshold
#         self.camera = videoSource(camera)
#         if display:
#             self.display = videoOutput('display://0')
#         self.net = detectNet(
#             model=self.model_path, labels=self.labels_path,
#             input_blob='input_0', output_cvg='scores',
#             output_bbox='boxes', threshold=self.threshold)

#     def detect(self):
#         """
#         Performs object detection on the captured image using the
#         network model.
#         Returns:
#             None
#         Raises:
#             None
#         """

#         while True:
#             image = self.camera.Capture()
#             detections = self.net.Detect(image)
#             if self.display:
#                 self.display.Render(image)
#                 self.display.SetStatus(
#                     f"Detection Network {self.net.GetNetworkFPS():.0f} FPS"
#                 )
#             if not self.camera.IsStreaming():
#                 break
#             return detections


# def main():
#     model_path = '/home/dipcar/DIPCar/data/models/ssd-mobilenet.onnx'
#     labels_path = '/home/dipcar/DIPCar/data/models/labels.txt'
#     detector = ObjectDetector(
#         model_path, labels_path,
#         camera="/dev/video0", display=True)
#     detections = detector.detect()
# if __name__ == "__main__":
#     main()
