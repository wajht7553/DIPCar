#!/usr/bin/python3
import time
import threading
from jetson_inference import detectNet, segNet
from src.control.enhanced_decision import DecisionMaker
from src.control.motor_controller import DIPCar
from jetson_utils import (videoSource, videoOutput,
                          cudaAllocMapped, cudaDeviceSynchronize)


def run_detection(camera, net, decision_maker, lock):
    while True:
        image = camera.Capture()
        detections = net.Detect(image, overlay='box,labels,lines')
        with lock:
            decision_maker.update_detections(detections)

def run_segmentation(camera, seg_net, decision_maker, lock):
    while True:
        image = camera.Capture()
        segmentation = seg_net.Process(image)
        with lock:
            decision_maker.update_segmentation(segmentation)


def main():
    camera = videoSource('/dev/video0')
    display = videoOutput('display://0')

    net = detectNet(
        model='data/models/detection/ssd-mobilenet.onnx',
        labels='data/models/detection/labels.txt',
        input_blob='input_0', output_cvg='scores',
        output_bbox='boxes', threshold=0.45
        )

    segnet = segNet(
        model="data/models/segmentation/fcn_resnet18.onnx",
        labels="data/models/segmentation/labels.txt",
        input_blob="input_0", output_blob="output_0"
    )

    dipcar = DIPCar()
    decision_maker = DecisionMaker(dipcar)

    lock = threading.Lock()

    det_thread = threading.Thread(
        target=run_detection,
        args=(camera, net, decision_maker, lock)
    )
    seg_thread = threading.Thread(
        target=run_segmentation,
        args=(camera, segnet, decision_maker, lock)
    )
    det_thread.start()
    seg_thread.start()

    try:
        while True:
            image = camera.Capture()
            decision_maker.make_decision()
            display.Render(image)
            display.SetStatus(
                f'Detecting Objects at {net.GetNetworkFPS():.0f} FPS'
                )
            end_time = time.time()
            if not camera.IsStreaming():
                print("Camera failure!!!")
                decision_maker.close()
                break
    except KeyboardInterrupt:
        dipcar.stop()
    finally:
        dipcar.cleanup()
        det_thread.join()
        seg_thread.join()


if __name__ == "__main__":
    main()
