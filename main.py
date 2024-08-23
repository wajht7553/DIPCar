import cv2
from src.perception.camera import Camera
from src.perception.object_detection import ObjectDetector
from src.custom_utils.visualizations import draw_detections
from src.control.motor_controller import DIPCar


def main():
    cam = Camera()
    detector = ObjectDetector("data/models/yolov5s.pt")
    dipcar = DIPCar()

    while True:
        frame = cam.capture_frame()
        detections = detector.detect_objects(frame)

        if len(detections.xyxy[0]) > 0:  # If any objects detected
            # Simple logic to avoid obstacles: stop if object detected
            dipcar.stop_motors()
        else:
            dipcar.forward(25)

        frame = draw_detections(frame, detections, detector.model.names)
        cv2.imshow('Autonomous Vehicle - Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
