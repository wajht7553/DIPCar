#!/usr/bin/python3
from jetson_inference import detectNet
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
    try:
        while True:
            image = camera.Capture()
            detections = net.Detect(image, overlay='box,labels,lines')
            display.Render(image)
            display.SetStatus(
                f'Detecting Objects at {net.GetNetworkFPS():.0f} FPS'
            )
            if not camera.IsStreaming():
                print("Camera failure!!!")
                break
    except KeyboardInterrupt:
        print("Program terminated by user!")


if __name__ == "__main__":
    main()
