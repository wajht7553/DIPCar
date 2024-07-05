import cv2
from src.perception.camera import Camera
from src.perception.object_detection import ObjectDetector
from src.custom_utils.visualiztions import draw_detections
from src.control.motor_control import MotorControl
from src.control.steering_control import SteeringControl


def main():
    cam = Camera()
    detector = ObjectDetector("data/models/yolov5s.pt")
    rear_motor = MotorControl(motor_pins=(13, 15), enable_pin=11)
    steering_motor = SteeringControl(motor_pins=(5, 7), enable_pin=3)

    while True:
        frame = cam.capture_frame()
        detections = detector.detect_objects(frame)

        if len(detections.xyxy[0]) > 0:  # If any objects detected
            # Simple logic to avoid obstacles: stop if object detected
            rear_motor.stop()
            steering_motor.stop()
        else:
            rear_motor.set_speed(1.0)  # Move forward
            steering_motor.steer("straight")

        frame = draw_detections(frame, detections, detector.model.names)
        cv2.imshow('Autonomous Vehicle - Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
