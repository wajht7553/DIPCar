import os
import cv2
from camera import Camera


# Parameters
output_dir = 'data/calibration/chessboard'
num_images = 20
camera_index = 1
counter = 0

# Create directory to store images
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Start capturing images
camera = Camera(camera_index)
print("Press 'c' to capture an image.")
while counter < num_images:
    success, frame = camera.read()
    if not success:
        print("Failed to capture image!\nCheck you camera connection.")
        break
    cv2.namedWindow('Capture Calibration Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Capture Calibration Image', 600, 400)
    cv2.imshow('Capture Calibration Image', frame)
    key = cv2.waitKey(1)
    if key == ord('c'):
        img_name = f'{output_dir}/image_{counter:02d}.png'
        cv2.imwrite(img_name, frame)
        print(f'Captured {img_name}')
        counter += 1
    if key == ord('q'):
        print('Interrupted by the user, exiting...')
        break
print(f'Finished, captured {counter} images.')
camera.close()
