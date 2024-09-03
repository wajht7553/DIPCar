#!/usr/bin/python3
from jetson.inference import detectNet
from jetson.utils import videoSource, videoOutput


net = detectNet(
    model='../../data/models/ssd-mobilenet.onnx',
    threshold=0.5
    )

camera = videoSource(
    '/dev/video0',
    argv=['--input-width=1280', '--input-height=720']
    )
display = videoOutput('display://0')
while display.isStreaming():
    img = camera.Capture()
    detections = net.Detect(img)
    display.Render(img)
    display.SetStatus(
        "Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

    for detection in detections:
        print(detection)
