import cv2
import numpy as np

def process_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use the Canny edge detector
    edges = cv2.Canny(blur, 50, 150)

    # Define a region of interest (ROI) mask
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # Only focus on the lower half of the screen
    polygon = np.array([[
        (0, height),
        (width, height),
        (width, height // 2),
        (0, height // 2),
    ]], np.int32)
    
    cv2.fillPoly(mask, polygon, 255)
    
    # Apply the mask to the edges image
    masked_edges = cv2.bitwise_and(edges, mask)

    # Use HoughLinesP to detect lines in the masked edge image
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, maxLineGap=50, minLineLength=100)

    # Create an image to draw the lines on
    line_image = np.zeros_like(frame)

    # Draw the lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)

    # Combine the original frame with the line image
    combined_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    return combined_image

def main(video_source=0):
    # Open the video file or camera feed
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        processed_frame = process_frame(frame)

        # Display the processed frame
        cv2.imshow('Road Edge Detection', processed_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close display windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 'video.mp4' with 0 for webcam or a file path for a video file
    main(video_source='test_road.mp4')
