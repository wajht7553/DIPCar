import argparse
from segnet_utils import *
from jetson_inference import segNet
from jetson_utils import (
                videoSource, videoOutput, cudaOverlay, cudaDeviceSynchronize
                )


def main():
    camera = videoSource('/dev/video0')
    display = videoOutput('display://0')
    args = argparse.Namespace(
        filter_mode='linear',
        visualize='overlay,mask',
        ignore_class='void',
        alpha='150.0',
        stats=False
    )
    net = segNet(
        model="data/models/segmentation/fcn_resnet34.onnx",
        labels="data/models/segmentation/labels.txt",
        input_blob="input_0", output_blob="output_0"
        )
    net.SetOverlayAlpha(150)
    buffers = SegmentationBuffers(net, args)

    # process frames until EOS or the user exits
    while True:
        # capture the next image
        image = camera.Capture()

        if image is None: # timeout
            continue
            
        # allocate buffers for this size image
        buffers.Alloc(image.shape, image.format)

        # process the segmentation network
        net.Process(image, ignore_class=args.ignore_class)

        # generate the overlay
        if buffers.overlay:
            net.Overlay(buffers.overlay, filter_mode=args.filter_mode)

        # generate the mask
        if buffers.mask:
            net.Mask(buffers.mask, filter_mode=args.filter_mode)

        # composite the images
        if buffers.composite:
            cudaOverlay(
                buffers.overlay,
                buffers.composite,
                0, 0
                )
            cudaOverlay(
                buffers.mask,
                buffers.composite,
                buffers.overlay.width, 0
                )

        # render the output image
        display.Render(buffers.output)

        # update the title bar
        display.SetStatus(
            f'Running Segmentation model at {net.GetNetworkFPS():.0f} FPS'
            )

        # print out performance info
        cudaDeviceSynchronize()
        net.PrintProfilerTimes()

        # compute segmentation class stats
        if args.stats:
            buffers.ComputeStats()

        # exit on input/output EOS
        if not camera.IsStreaming() or not display.IsStreaming():
            break

if __name__ == "__main__":
    main()
