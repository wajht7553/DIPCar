import cv2
import torch
from src.perception.camera import Camera
from src.custom_utils.visualiztions import draw_detections

class ObjectDetector:
    def __init__(self, model_path='../../data/models/yolov5s.pt'):
        self.model = torch.hub.load('ultralytics/yolov5',
                                    'custom', path=model_path)

    def detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        for *box, conf, cls in results.xyxy[0]:
            detections.append({
                "box": (int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1])),
                "confidence": float(conf),
                "class_id": int(cls)
            })
        return detections


# Example usage:
if __name__ == "__main__":
    detector = ObjectDetector()
    cam = Camera()
    while True:
        frame = cam.capture_frame()
        detections = detector.detect_objects(frame)
        frame = draw_detections(frame, detections, detector.model.names)
        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
