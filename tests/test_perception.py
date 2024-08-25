import unittest
from src.perception.utils.camera import Camera
from src.perception.object_detection import ObjectDetector


class TestCamera(unittest.TestCase):
    def test_camera_initialization(self):
        camera = Camera()
        self.assertIsNotNone(camera.cap)

    def test_capture_frame(self):
        camera = Camera()
        frame = camera.capture_frame()
        self.assertEqual(len(frame.shape), 3)
        camera.close()


class TestObjectDetection(unittest.TestCase):
    def test_object_detection_initialization(self):
        detector = ObjectDetector("../data/models/yolov5s.pt")
        self.assertIsNotNone(detector.model)

    def test_detect_objects(self):
        detector = ObjectDetector("../data/models/yolov5s.pt")
        camera = Camera()
        frame = camera.capture_frame()
        detections = detector.detect_objects(frame)
        self.assertIsInstance(detections, list)
        camera.close()


if __name__ == "__main__":
    unittest.main()
