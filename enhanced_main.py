#!/usr/bin/python3
import time
import argparse
from segnet_utils import SegmentationBuffers
from jetson_inference import detectNet, segNet
from src.control.decision import DecisionMaker
from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput, cudaOverlay, cudaToNumpy
# import cv2


def main():
    camera = videoSource('/dev/video0')
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

            # Convert CudaImage to numpy array
            np_image = cudaToNumpy(image)

            # Display the image in a separate window
            # cv2.imshow('Captured Image', np_image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # Run detection
            detections = det_net.Detect(image, overlay='box,labels,lines')

            # Run segmentation
            buffers.Alloc(image.shape, image.format)
            seg_net.Process(image, ignore_class=args.ignore_class)

            if buffers.overlay:
                seg_net.Overlay(buffers.overlay, filter_mode=args.filter_mode)

            if buffers.mask:
                seg_net.Mask(buffers.mask, filter_mode=args.filter_mode)

            # Simple steering control based on segmentation mask
            # road_center = analyze_road_center(buffers.mask)
            # steer_car(dipcar, road_center)

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
        # cv2.destroyAllWindows()
        # dipcar.cleanup()
        pass


def analyze_road_center(mask):
    # Simple analysis: check the bottom half of the image
    height, width = mask.shape
    bottom_half = mask[height//2:, :]
    left_sum = bottom_half[:, :width//2].sum()
    right_sum = bottom_half[:, width//2:].sum()

    if left_sum > right_sum:
        return 'left'
    elif right_sum > left_sum:
        return 'right'
    else:
        return 'center'


def steer_car(dipcar, road_center):
    if road_center == 'left':
        dipcar.steer_left(25)
    elif road_center == 'right':
        dipcar.steer_right(25)
    # If center, the decision_maker will handle forward motion


if __name__ == "__main__":
    main()
