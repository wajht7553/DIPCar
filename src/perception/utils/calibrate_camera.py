import cv2
import glob
import numpy as np


def create_object_points(pattern_size):
    """
    Create object points for calibration using circles grid.
    Parameters:
        pattern_size (tuple): The size of the pattern grid.
    Returns:
        np.ndarray: The object points for calibration.
    """

    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0],
                           0:pattern_size[1]].T.reshape(-1, 2)
    return objp

def calibrate_camera(images_dir, pattern_size, object_points):
    """
    Calibrates the camera using a set of images, a pattern size, and object points.
    Parameters:
        images_dir (str): A string representing the images path.
        pattern_size (tuple): The size of the pattern used for
            calibration.
        object_points (list): A list of object points corresponding
            to the pattern.
    Returns:
        mtx (ndarray): The camera matrix
        dist (ndarray): The distortion coefficients.
        rvecs (list): A list of rotation vectors.
        tvecs (list): A list of translation vectors.
    """
    obj_points = []
    img_points = []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    images = glob.glob(f'{images_dir}/*.png')

    for file_name in images:
        image = cv2.imread(file_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(
            gray, pattern_size, None)
        corners = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)
        
        if ret:
            obj_points.append(object_points)
            img_points.append(corners)
            image = cv2.drawChessboardCorners(image, pattern_size, corners, ret)
            cv2.imshow('Calibration', image)
            cv2.waitKey(100)

    cv2.destroyAllWindows()
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, gray.shape[::-1], None, None)
    return camera_matrix, dist_coeffs, rvecs, tvecs, obj_points, img_points


def main():
    images_dir = 'data/calibration/chessboard'
    pattern_size = (7, 10)

    object_points = create_object_points(pattern_size)
    camera_matrix, dist_coeffs, rvecs, tvecs, obj_points, img_points = calibrate_camera(
        images_dir, pattern_size, object_points
    )

    # Save calibration results
    np.savez(f'{images_dir}/calibration_data.npz',
                camera_matrix=camera_matrix, dist_coeffs=dist_coeffs,
                rvecs=rvecs, tvecs=tvecs, pattern_size=pattern_size,
                object_points=obj_points, image_points=img_points)

    print("Camera calibrated successfully.")
    print("Camera matrix:\n", camera_matrix)
    print("Distortion coefficients:\n", dist_coeffs)

if __name__ == "__main__":
    main()
