#!/usr/bin/python3
import time
from jetson_inference import detectNet
from src.control.decision import DecisionMaker
from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput


def main():
    camera = videoSource('/dev/video0')
    display = videoOutput('display://0')
    net = detectNet(
        model='data/models/detection/ssd-mobilenet.onnx',
        labels='data/models/detection/labels.txt',
        input_blob='input_0', output_cvg='scores',
        output_bbox='boxes', threshold=0.45
        )
    time.sleep(5)
    dipcar = DIPCar()
    decision_maker = DecisionMaker(dipcar)
    try:
        while True:
            start_time = time.time()
            image = camera.Capture()
            detections = net.Detect(image, overlay='box,labels,lines')
            decision_maker.make_decision(detections)
            display.Render(image)
            display.SetStatus(
                f'Detecting Objects at {net.GetNetworkFPS():.0f} FPS'
                )
            end_time = time.time()
            print(f"latency: {end_time-start_time}")
            if not camera.IsStreaming():
                print("Camera failure!!!")
                decision_maker.close()
                break
        dipcar.cleanup()
    except KeyboardInterrupt:
        dipcar.cleanup()


if __name__ == "__main__":
    main()
