import cv2

class Camera:
    """
    A class to represent camera connected either through CSI or USB


    Attributes:
        camera_id (int): the id of the camera if USB camera is being used
        width (int): The width of the captured frame
        height (int): The height of the captured frame
        fps (int): The number of frames in case of video stream. Be careful as high resolutions doesn't support high fps
        flip (int): how to flip the captured stream
    """    
    def __init__(self, camera_id=0, width=1920, height=1080, fps=30, flip=0):
        """
        Initialize the various attributes
        """      
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.flip = flip
        self.cap = cv2.VideoCapture(self._gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    def _gstreamer_pipeline(self):
        """Create a GStreamer pipline

        Returns:
            String: a string that represents the various parameters of the pipeline
        """        
        return (
            f"nvarguscamerasrc ! "
            f"video/x-raw(memory:NVMM), "
            f"width={self.width}, height={self.height}, "
            f"format=NV12, framerate={self.fps}/1 ! "
            f"nvvidconv flip-method={self.flip} ! "
            f"video/x-raw, width=1280, height=720, format=BGRx ! "
            f"videoconvert ! "
            f"video/x-raw, format=BGR ! appsink"
                )         

    def capture_frame(self):
        """Capture a single frame

        Raises:
            Exception: raise an exception if it fails to capture a frame

        Returns:
            image: the captured frame as a numpy array
        """        
        success, frame = self.cap.read()
        if not success:
            raise Exception("Failed to capture image")
        return frame

    def release(self):
        """Release the pipeline
        """        
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
