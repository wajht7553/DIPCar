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
    video_path = '../test_road_2.mp4'
    camera = videoSource(video_path)
    display = videoOutput('display://0')

    if not camera.IsStreaming():
        print("Failed to open video source!")
        return

    # Detection model setup
    det_net = detectNet(
        model='data/models/detection/ssd-mobilenet.onnx',
        labels='data/models/detection/labels.txt',
        input_blob='input_0',
        output_cvg='scores',
        output_bbox='boxes'
    )

    # Segmentation model setup
    seg_net = segNet(
        model='data/models/segmentation/fcn-resnet18.onnx',
        labels='data/models/segmentation/labels.txt',
        input_blob='input_0',
        output_blob='output_0'
    )

    buffers = SegmentationBuffers()

    while display.IsStreaming():
        image = camera.Capture()
        if image is None:
            print("Failed to capture image!")
            break

        # Run segmentation
        buffers.Alloc(image.shape, image.format)
        seg_net.Process(image, ignore_class=None)

        if buffers.overlay:
            seg_net.Overlay(buffers.overlay, filter_mode='linear')

        if buffers.mask:
            seg_net.Mask(buffers.mask, filter_mode='linear')

        # Convert CudaImage to numpy array
        np_image = cudaToNumpy(buffers.mask)
        np_image = np_image[:, :, ::-1]
        np_image_gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        _, binary_mask = cv2.threshold(np_image_gray, 56, 255, cv2.THRESH_BINARY)
        steering_angle = calculate_steering_angle(binary_mask)
        print(f'Steering angle: {steering_angle:.2f}')

        # Render output
        if buffers.composite:
            cudaOverlay(buffers.overlay, image, 0, 0)
        display.Render(image)
        display.SetStatus(f'Segmentation | Network {seg_net.GetNetworkFPS():.0f} FPS')

    camera.Close()
    display.Close()

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
