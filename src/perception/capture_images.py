import os
import cv2
from camera import Camera

# Parameters
output_dir = 'src/perception/calibration_images'
num_images = 20
camera_index = 1

# Create directory to store images
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Start capturing images
camera = Camera(camera_index)
print("Press 'c' to capture an image.")

counter = 0
while counter < num_images:
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image")
        break

    cv2.imshow('Capture Calibration Image', frame)

    # Capture image when 'c' key is pressed
    key = cv2.waitKey(1)
    if key == ord('c'):
        img_name = f'{output_dir}/image_{counter:02d}.png'
        cv2.imwrite(img_name, frame)
        print(f'Captured {img_name}')
        counter += 1

camera.release()
cv2.destroyAllWindows()
