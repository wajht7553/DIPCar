import cv2


def draw_detections(frame, detections, class_names):
    for detection in detections:
        x, y, w, h = detection["box"]
        label = f"{class_names[detection['class_id']]} {detection['confidence']:.2f}"
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame
