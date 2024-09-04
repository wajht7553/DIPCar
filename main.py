#!/usr/bin/python3
from jetson_inference import detectNet
from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput


def main():
    frame_options = {
        'width': 1280,
        'height': 720,
        'fps': 24,
    }
    camera = videoSource('/dev/video0', options=frame_options)
    display = videoOutput('display://0')
    dipcar = DIPCar()
    dipcar.forward(25)
    net = detectNet(
        model='data/models/ssd-mobilenet.onnx',
        labels='data/models/labels.txt',
        input_blob='input_0', output_cvg='scores', output_bbox='boxes',
        )

    while True:
        image = camera.Capture()
        detections = net.Detect(image)
        display.Render(image)
        display.SetStatus(
            f'Detecting Objects at {net.GetNetworkFPS():.0f} FPS'
        )
        for detection in detections:
            class_id = detection.ClassID
            confidence = detection.Confidence
            class_name = net.GetClassDesc(class_id)
            print(f"Detected {class_name} with confidence {confidence:.2f}")

            if class_name == "stop" and confidence > 0.5:
                print("Stop sign detected! Stopping motors.")
                dipcar.stop()

        if not camera.IsStreaming():
            break

if __name__ == "__main__":
    main()
