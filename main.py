#!/usr/bin/python3
from jetson_inference import detectNet
# from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput


def main():
    camera = videoSource('/dev/video0')
    display = videoOutput('display://0')
    net = detectNet(
        model='data/models/ssd-mobilenet.onnx',
        labels='data/models/labels.txt',
        input_blob='input_0', output_cvg='scores', output_bbox='boxes',
        )
    # dipcar = DIPCar()

    while True:
        image = camera.Capture()
        detections = net.Detect(image)
        display.Render(image)
        display.SetStatus(
            f'Detecting Objects at {net.GetNetworkFPS():.0f} FPS'
        )
        for detection in detections:
            print(detection.Area)
        if not camera.IsStreaming():
            break

if __name__ == "__main__":
    main()
