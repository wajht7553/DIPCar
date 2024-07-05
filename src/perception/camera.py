import cv2


class Camera:
    def __init__(self, camera_id=0, width=1280, height=720):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def capture_frame(self):
        success, frame = self.cap.read()
        if not success:
            raise Exception("Failed to capture image")
        return frame

    def release(self):
        self.cap.release()


# Example usage:
if __name__ == "__main__":
    camera = Camera()
    while True:
        frame = camera.capture_frame()
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

# =============================================================================#


# import cv2

# class Camera:
#     def __init__(self, camera_id=0, width=1280, height=720):
#         self.camera_id = camera_id
#         self.width = width
#         self.height = height
#         self.cap = cv2.VideoCapture(self._gstreamer_pipeline(), cv2.CAP_GSTREAMER)

#     def _gstreamer_pipeline(self):
#         return (
#             f"nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int){self.width}, height=(int){self.height}, "
#             f"format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=2 ! "
#             f"video/x-raw, width=(int){self.width}, height=(int){self.height}, format=(string)BGRx ! "
#             f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
#         )

#     def capture_frame(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             raise Exception("Failed to capture image")
#         return frame

#     def release(self):
#         self.cap.release()

# # Example usage:
# if __name__ == "__main__":
#     camera = Camera()
#     while True:
#         frame = camera.capture_frame()
#         cv2.imshow('Camera Feed', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     camera.release()
#     cv2.destroyAllWindows()
