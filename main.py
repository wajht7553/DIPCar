#!/usr/bin/python3
import cv2
import time
import argparse
from segnet_utils import SegmentationBuffers
from jetson_inference import detectNet, segNet
from src.control.decision import DecisionMaker
from src.control.motor_controller import DIPCar
from jetson_utils import (
    videoSource, videoOutput,
    cudaOverlay, cudaToNumpy,
)
from src.perception.road_utils import (
    get_steering_angle,add_direction_line
)


def main():
    input_options = {
        "width": 640,
        "height": 480,
    }
    input_src = videoSource('/dev/video0', options=input_options)
    display = videoOutput('display://0')

    det_net = detectNet(
        model="data/models/detection/ssd-mobilenet.onnx",
        labels="data/models/detection/labels.txt",
        input_blob="input_0",
        output_cvg="scores",
        output_bbox="boxes",
        threshold=0.45,
    )
    seg_net = segNet(
        model="data/models/segmentation/fcn_resnet34.onnx",
        labels="data/models/segmentation/labels.txt",
        input_blob="input_0",
        output_blob="output_0",
    )

    args = argparse.Namespace(
        filter_mode="linear",
        visualize="overlay,mask",
        ignore_class="void",
        alpha="150.0",
        stats=True,
    )

    seg_net.SetOverlayAlpha(150)
    buffers = SegmentationBuffers(seg_net, args)

    dipcar = DIPCar()
    decision_maker = DecisionMaker(dipcar)

    try:
        while True:
            image = input_src.Capture()
            detections = det_net.Detect(image, overlay='box,labels,lines')
            buffers.Alloc(image.shape, image.format)
            seg_net.Process(image, ignore_class=args.ignore_class)

            if buffers.overlay:
                seg_net.Overlay(buffers.overlay, filter_mode=args.filter_mode)

            if buffers.mask:
                seg_net.Mask(buffers.mask, filter_mode=args.filter_mode)

            _, binary_mask = cv2.threshold(
                cv2.cvtColor(cudaToNumpy(buffers.mask), cv2.COLOR_BGR2GRAY),
                128, 255, cv2.THRESH_BINARY
            )
            print(f'Steering angle: {get_steering_angle(binary_mask):.2f} degrees.')
            buffers.mask = add_direction_line(buffers.mask, binary_mask)

            decision_maker.make_decision(detections)

            if buffers.composite:
                cudaOverlay(buffers.overlay, buffers.composite, 0, 0)
                cudaOverlay(buffers.mask, buffers.composite, buffers.overlay.width, 0)
                display.render(buffers.composite)
            else:
                display.Render(image)
            display.SetStatus(
                f"Detection: {det_net.GetNetworkFPS():.0f} FPS, Segmentation: {seg_net.GetNetworkFPS():.0f} FPS"
            )
            if not input_src.IsStreaming():
                print("Input failure!!!")
                break
    except KeyboardInterrupt:
        print('Program terminated by user, Exiting...')
    finally:
        decision_maker.close()
        dipcar.cleanup()


if __name__ == "__main__":
    main()
