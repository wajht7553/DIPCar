#!/usr/bin/python3
import cv2
import time
import argparse
import numpy as np
from segnet_utils import SegmentationBuffers
from jetson_inference import detectNet, segNet
from src.control.decision import DecisionMaker
from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput, cudaOverlay, cudaToNumpy


def main():
    input_options = {
        'width': 640,
        'height': 480,
    }
    camera = videoSource('/dev/video0', options=input_options)
    display = videoOutput('display://0')

    # Detection model setup
    det_net = detectNet(
        model='data/models/detection/ssd-mobilenet.onnx',
        labels='data/models/detection/labels.txt',
        input_blob='input_0', output_cvg='scores',
        output_bbox='boxes', threshold=0.45
    )

    # Segmentation model setup
    args = argparse.Namespace(
        filter_mode='linear',
        visualize='overlay,mask',
        ignore_class='void',
        alpha='150.0',
        stats=True
    )
    seg_net = segNet(
        model="data/models/segmentation/fcn_resnet34.onnx",
        labels="data/models/segmentation/labels.txt",
        input_blob="input_0", output_blob="output_0"
    )
    seg_net.SetOverlayAlpha(150)
    buffers = SegmentationBuffers(seg_net, args)

    # dipcar = DIPCar()
    # decision_maker = DecisionMaker(dipcar)

    try:
        while True:
            # Capture image
            image = camera.Capture()

            # Run detection
            detections = det_net.Detect(image, overlay='box,labels,lines')

            # Run segmentation
            buffers.Alloc(image.shape, image.format)
            seg_net.Process(image, ignore_class=args.ignore_class)

            if buffers.overlay:
                seg_net.Overlay(buffers.overlay, filter_mode=args.filter_mode)

            if buffers.mask:
                seg_net.Mask(buffers.mask, filter_mode=args.filter_mode)
            # Convert CudaImage to numpy array
            np_image = cudaToNumpy(buffers.mask)
            np_image = np_image[:, :, ::-1]
            np_image_gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
            _, binary_mask = cv2.threshold(np_image_gray, 56, 255, cv2.THRESH_BINARY)
            steering_angle = calculate_steering_angle(binary_mask)
            print(f'Steering angle: {steering_angle:.2f}')

            # Make decision based on detections
            # decision_maker.make_decision(detections)

            # Render output
            if buffers.composite:
                cudaOverlay(buffers.overlay, buffers.composite, 0, 0)
                cudaOverlay(buffers.mask, buffers.composite,
                            buffers.overlay.width, 0)
                display.Render(buffers.output)
            else:
                display.Render(image)

            display.SetStatus(
                f'Detection: {det_net.GetNetworkFPS():.0f} FPS, Segmentation: {seg_net.GetNetworkFPS():.0f} FPS'
            )

            if not camera.IsStreaming():
                print("Camera failure!!!")
                # decision_maker.close()
                break

        # dipcar.cleanup()
    except KeyboardInterrupt:
        print('Program terminated by user!')
    finally:
        # dipcar.cleanup()
        pass


def calculate_steering_angle(binary_mask):
    # Calculate the centroid of the white pixels (road)
    moments = cv2.moments(binary_mask)
    if moments["m00"] == 0:
        return 0  # Default to 0 if no road detected

    cx = int(moments["m10"] / moments["m00"])
    image_width = binary_mask.shape[1]

    # Calculate the deviation from the center
    deviation = cx - (image_width // 2)

    # Simple proportional control for steering
    steering_angle = -deviation / (image_width // 2) * 45  # Scale to degrees

    return steering_angle


if __name__ == "__main__":
    main()
