import cv2
import numpy as np
from camera import Camera


def load_calibration(calibration_file):
    """
    Load calibration data from a file.
    Parameters:
        calibration_file (str): The path to the calibration file.
    Returns:
        mtx (ndarray): The camera matrix.
        dist (ndarray): The distortion coefficients.
        rvecs (list): A list of rotation vectors.
        tvecs (list): A list of translation vectors.
        objpoints (list): A list of object points.
        imgpoints (list): A list of image points.
    """
    with np.load(calibration_file) as data:
        camera_matrix = data['camera_matrix']
        dist_coeffs = data['dist_coeffs']
        rvecs = data['rvecs']
        tvecs = data['tvecs']
        pattern_size = tuple(data['pattern_size'])
        objpoints = data['object_points']
        imgpoints = data['image_points']
    return (camera_matrix, dist_coeffs, rvecs, tvecs,
            pattern_size, objpoints, imgpoints)


def compute_reprojection_error(camera_matrix, dist_coeffs,
                               rvecs, tvecs, objpoints, imgpoints):
    """
    Compute the reprojection error of the calibration.
    Parameters:
        camera_matrix (ndarray): The camera matrix.
        dist_coeffs (ndarray): The distortion coefficients.
        rvecs (list): A list of rotation vectors.
        tvecs (list): A list of translation vectors.
        objpoints (list): A list of object points.
        imgpoints (list): A list of image points.
    Returns:
        mean_error (float): The mean reprojection error.
    """
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
        error = cv2.norm(imgpoints[i], imgpoints2,
                         cv2.NORM_L2) / len(imgpoints2)
        total_error += error

    mean_error = total_error / len(objpoints)
    return mean_error


def validate_calibration(camera, camera_matrix, dist_coeffs, pattern_size):
    """
    Validates the calibration of a camera using a chessboard pattern.
    Parameters:
        camera: The camera object used for capturing frames.
        camera_matrix: The camera matrix used for undistorting frames.
        dist_coeffs: The distortion coefficients used for undistorting frames.
        pattern_size: The size of the chessboard pattern used for calibration.
    Returns:
        None
    """

    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to grab frame")
            break

        undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_undist = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

        ret_orig, corners_orig = cv2.findChessboardCorners(
            gray, pattern_size, None)
        ret_undist, corners_undist = cv2.findChessboardCorners(
            gray_undist, pattern_size, None)

        if ret_orig and ret_undist:
            cv2.drawChessboardCorners(
                frame, pattern_size, corners_orig, ret_orig)
            cv2.drawChessboardCorners(
                undistorted, pattern_size, corners_undist, ret_undist)

        cv2.imshow("Original", frame)
        cv2.imshow("Undistorted", undistorted)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    calibration_file = f'data/calibration/chessboard/calibration_data.npz'
    camera_index = 1
    camera = Camera(camera_index)
    camera_matrix, dist_coeffs, rvecs, tvecs, pattern_size, objpoints, imgpoints = load_calibration(
        calibration_file)
    reprojection_error = compute_reprojection_error(
        camera_matrix, dist_coeffs, rvecs, tvecs, objpoints, imgpoints)
    print(f'Reprojection error: {reprojection_error}')
    validate_calibration(camera, camera_matrix, dist_coeffs, pattern_size)
    camera.close()


if __name__ == "__main__":
    main()
