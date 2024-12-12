#!/usr/bin/python3
import cv2


class Camera:
    """
    Initialize the Camera object.
    Args:
        source (int or str): The source of the camera. It can be an integer representing the camera index or a string representing the video file path.
        width (int): The width of the captured frame in pixels. Default is 1920.
        height (int): The height of the captured frame in pixels. Default is 1080.
        fps (int): The frames per second of the captured frame. Default is 30.
        flip (int): The flip method of the captured frame. Default is 0.
    """

    def __init__(self, source=0, width=1920, height=1080, fps=24, flip=0):
        """
        Initializes the Camera object.
        Parameters:
            source (int or str): The source of the camera.
                It can be either an integer representing the camera
                index or a string representing the video file path.
            width (int): The width of the camera frame.
            height (int): The height of the camera frame.
            fps (int): The frames per second of the camera.
            flip (int): The flip code for the camera frame.
        Returns:
            None
        """

        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        self.flip = flip
        # self.cap = cv2.VideoCapture(
        #     self._gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        self.cap = cv2.VideoCapture(self.source)

    def _gstreamer_pipeline(self):
        """
        Returns the GStreamer pipeline string for capturing video using the nvarguscamerasrc element.
        Returns:
            str: The GStreamer pipeline string.
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

    def read(self):
        """
        Reads a frame from the camera.
        Returns:
            success (bool): True if the frame was successfully read,
                False otherwise.
            frame: The captured frame from the camera.
        """

        success, frame = self.cap.read()
        return success, frame

    def close(self):
        """
        Closes the camera by releasing the capture
        and destroying any open windows.
        Args:
            None
        Returns:
            None
        """

        self.cap.release()
        cv2.destroyAllWindows()
