import cv2
import numpy as np
from jetson_utils import cudaToNumpy, cudaFromNumpy


def get_road_direction(binary_mask):
    """
    Calculate road direction with enhanced stability and directional bias

    Args:
        binary_mask (np.ndarray): Binary road segmentation mask

    Returns:
        np.ndarray: Normalized direction vector
    """
    # Get road pixels
    road_pixels = np.column_stack(np.where(binary_mask > 0))

    # If no road pixels, return default forward direction
    if len(road_pixels) == 0:
        return np.array([0, -1])  # Pointing forward

    # Compute bottom half of road pixels for more stable direction
    height = binary_mask.shape[0]
    bottom_half_pixels = road_pixels[road_pixels[:, 0] > height // 2]

    if len(bottom_half_pixels) == 0:
        bottom_half_pixels = road_pixels

    # Weighted linear regression to get direction
    X = bottom_half_pixels[:, 1]
    Y = bottom_half_pixels[:, 0]

    # Weighted linear regression
    weights = (Y - height) / height  # More weight to bottom pixels
    weights = np.abs(weights)

    # Fit line using weighted regression
    coeffs = np.polyfit(X, Y, deg=1, w=weights)

    # Direction vector from line slope
    slope = coeffs[0]
    direction = np.array([-slope, -1])

    # Normalize direction
    norm = np.linalg.norm(direction)
    return direction / norm if norm > 0 else np.array([0, -1])


def add_direction_line(cuda_image, binary_mask):
    """
    Adds a road direction line to the given CUDA image based on the provided binary mask.
    Args:
        cuda_image: The input image in CUDA format.
        binary_mask: A binary mask indicating the road area.
    Returns:
        The CUDA image with the road direction line drawn on it.
    """

    np_image = cudaToNumpy(cuda_image)
    height, width, _ = np_image.shape

    # Calculate road direction
    direction_vector = get_road_direction(binary_mask)

    # Start point: bottom middle of image
    start_point = (width // 2, height - 1)

    # Calculate end point with fixed length
    line_length = height // 2
    end_point = (
        int(start_point[0] + direction_vector[0] * line_length),
        int(start_point[1] + direction_vector[1] * line_length),
    )

    # Draw line on the image
    cv2.line(np_image, start_point, end_point, (0, 0, 255), 3)

    return cudaFromNumpy(np_image)


def get_steering_angle(binary_mask):
    """
    Calculate the steering angle based on the provided binary mask of the road.
    This function computes the moments of the binary mask to find the centroid
    of the detected road area. It then calculates the deviation of the centroid
    from the center of the image and uses a simple proportional control to 
    determine the steering angle.
    Args:
        binary_mask (numpy.ndarray): A binary image where the road is marked 
                                     with white pixels (255) and the background 
                                     is black (0).
    Returns:
        float: The calculated steering angle in degrees. A positive value 
               indicates a right turn, and a negative value indicates a left turn.
               Returns 0 if no road is detected.
    """

    moments = cv2.moments(binary_mask)
    if moments["m00"] == 0:
        return 0  # Default to 0 if no road detected

    cx = int(moments["m10"] / moments["m00"])
    image_width = binary_mask.shape[1]

    # Calculate the deviation from the center
    deviation = cx - (image_width // 2)

    # Simple proportional control for steering
    steering_angle = -deviation / (image_width // 2) * 45  # Scale to degrees

    return steering_angle
