#!/usr/bin/python3
import cv2
import argparse
import numpy as np
from segnet_utils import SegmentationBuffers
from jetson_inference import detectNet, segNet
from jetson_utils import (
    videoSource, videoOutput,
    cudaOverlay, cudaToNumpy,
)
from src.perception.road_utils import (
    get_steering_angle,
    add_direction_line
)


def main():
    input_options = {
        "width": 640,
        "height": 480,
    }
    camera = videoSource("../test_road_2.mp4", options=input_options)
    display = videoOutput("display://0")

    # Detection and segmentation model setup (unchanged)
    det_net = detectNet(
        model="data/models/detection/ssd-mobilenet.onnx",
        labels="data/models/detection/labels.txt",
        input_blob="input_0",
        output_cvg="scores",
        output_bbox="boxes",
        threshold=0.45,
    )

    args = argparse.Namespace(
        filter_mode="linear",
        visualize="overlay,mask",
        ignore_class="void",
        alpha="150.0",
        stats=True,
    )
    seg_net = segNet(
        model="data/models/segmentation/fcn_resnet34.onnx",
        labels="data/models/segmentation/labels.txt",
        input_blob="input_0",
        output_blob="output_0",
    )
    seg_net.SetOverlayAlpha(150)
    buffers = SegmentationBuffers(seg_net, args)

    try:
        while True:
            # Capture image
            image = camera.Capture()

            # Run detection and segmentation
            detections = det_net.Detect(image, overlay="box,labels,lines")
            buffers.Alloc(image.shape, image.format)
            seg_net.Process(image, ignore_class=args.ignore_class)

            if buffers.overlay:
                seg_net.Overlay(buffers.overlay, filter_mode=args.filter_mode)

            if buffers.mask:
                seg_net.Mask(buffers.mask, filter_mode=args.filter_mode)

            # Convert mask to binary
            np_image = cudaToNumpy(buffers.mask)
            np_image_gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
            _, binary_mask = cv2.threshold(np_image_gray, 56, 255, cv2.THRESH_BINARY)

            print(f'Steering angle: {get_steering_angle(binary_mask):.2f} degrees')
            # Add road direction line directly to mask
            buffers.mask = add_direction_line(buffers.mask, binary_mask)

            # Render output
            if buffers.composite:
                cudaOverlay(buffers.overlay, buffers.composite, 0, 0)
                cudaOverlay(buffers.mask, buffers.composite, buffers.overlay.width, 0)
                display.Render(buffers.output)
            else:
                display.Render(image)

            display.SetStatus(
                f"Detection: {det_net.GetNetworkFPS():.0f} FPS, Segmentation: {seg_net.GetNetworkFPS():.0f} FPS"
            )

            if not camera.IsStreaming():
                print("Camera failure!!!")
                break

    except KeyboardInterrupt:
        print("Program terminated by user!")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
