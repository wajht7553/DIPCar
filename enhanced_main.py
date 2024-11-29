#!/usr/bin/python3
import cv2
import numpy as np
import argparse
from jetson_inference import detectNet, segNet
from jetson_utils import (
    videoSource,
    videoOutput,
    cudaOverlay,
    cudaToNumpy,
    cudaFromNumpy,
)
from segnet_utils import SegmentationBuffers


# Add straight line to the road direction

def calculate_road_direction(binary_mask):
    """
    Calculate road direction with enhanced stability and directional bias

    Args:
        binary_mask (np.ndarray): Binary road segmentation mask

    Returns:
        np.ndarray: Normalized direction vector
    """
    # Get road pixels
    road_pixels = np.column_stack(np.where(binary_mask > 0))

    # If no road pixels, return default forward direction
    if len(road_pixels) == 0:
        return np.array([0, -1])  # Pointing forward

    # Compute bottom half of road pixels for more stable direction
    height = binary_mask.shape[0]
    bottom_half_pixels = road_pixels[road_pixels[:, 0] > height // 2]

    if len(bottom_half_pixels) == 0:
        bottom_half_pixels = road_pixels

    # Weighted linear regression to get direction
    X = bottom_half_pixels[:, 1]
    Y = bottom_half_pixels[:, 0]

    # Weighted linear regression
    weights = (Y - height) / height  # More weight to bottom pixels
    weights = np.abs(weights)

    # Fit line using weighted regression
    coeffs = np.polyfit(X, Y, deg=1, w=weights)

    # Direction vector from line slope
    slope = coeffs[0]
    direction = np.array([-slope, -1])

    # Normalize direction
    norm = np.linalg.norm(direction)
    return direction / norm if norm > 0 else np.array([0, -1])


def add_road_direction_line(cuda_image, binary_mask):
    """Add road direction line to CUDA image with enhanced stability"""
    np_image = cudaToNumpy(cuda_image)
    height, width, _ = np_image.shape

    # Calculate road direction
    direction_vector = calculate_road_direction(binary_mask)

    # Start point: bottom middle of image
    start_point = (width // 2, height - 1)

    # Calculate end point with fixed length
    line_length = height // 2
    end_point = (
        int(start_point[0] + direction_vector[0] * line_length),
        int(start_point[1] + direction_vector[1] * line_length),
    )

    # Draw line on the image
    cv2.line(np_image, start_point, end_point, (0, 0, 255), 3)

    return cudaFromNumpy(np_image)


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

            print(f'Steering angle: {calculate_steering_angle(binary_mask):.2f} degrees')
            # Add road direction line directly to mask
            buffers.mask = add_road_direction_line(buffers.mask, binary_mask)

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
