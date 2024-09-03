import cv2

from src.perception.utils.camera import Camera
from src.control.motor_controller import DIPCar
from jetson_utils import videoSource, videoOutput
from src.perception.object_detection import ObjectDetector


def main():
    camera = '/dev/video0'
    display = True
    detector = ObjectDetector(
        model_path='/home/dipcar/DIPCar/data/models/ssd-mobilenet.onnx',
        labels_path='/home/dipcar/DIPCar/data/models/labels.txt',
        camera=camera, display=display
        )
    dipcar = DIPCar()

    


if __name__ == "__main__":
    main()
