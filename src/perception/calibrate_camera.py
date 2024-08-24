import cv2
import glob
import numpy as np

# Parameters
# Number of inner corners per a chessboard row and column
chessboard_size = (6, 9)
square_size = 1.0  # Size of a square in your defined unit (e.g., millimeters)
calibration_images_dir = 'src\perception\calibration_images\*.png'

# Termination criteria for cornerSubPix
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points based on the actual size of the checkerboard squares
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3d points in real-world space
imgpoints = []  # 2d points in image plane

# Load images and find corners
images = glob.glob(calibration_images_dir)
for file_name in images:
    print(file_name)
    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(
        gray, chessboard_size,)
    print(f'corners: {corners}')
    # If found, refine the corners and add to the list
    if ret:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('Calibration', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()
# Perform camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the calibration results
np.savez('src/perception/calibration_data.npz', camera_matrix=camera_matrix,
         dist_coeffs=dist_coeffs, rvecs=rvecs, tvecs=tvecs)

print("Camera calibrated successfully.")
print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)
