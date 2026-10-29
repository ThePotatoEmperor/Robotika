from ctu_bosch_sr450 import RobotBosch
import cv2

robot = RobotBosch()
robot.initialize()

robot.move_to_q([-0.4,0,0,0])
robot.wait_for_motion_stop()

img = robot.grab_image()

if img is not None:
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 800, 600)

    cv2.imshow("Camera", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Could not capture an image.")

# img is the original image from robot.grab_image()
preview = img.copy()

families = [
    "DICT_4X4_1000",
    "DICT_5X5_1000",
    "DICT_6X6_1000",
    "DICT_7X7_1000",
    "DICT_ARUCO_ORIGINAL",
    "DICT_APRILTAG_16h5",
    "DICT_APRILTAG_25h9",
    "DICT_APRILTAG_36h10",
    "DICT_APRILTAG_36h11",
]

dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_1000
)
detector = cv2.aruco.ArucoDetector(dictionary)

corners, ids, _ = detector.detectMarkers(img)


markers = {}

if ids is not None:
    cv2.aruco.drawDetectedMarkers(preview, corners, ids)

    for marker_corners, marker_id in zip(corners, ids.flatten()):
        marker_id = int(marker_id)
        points = marker_corners.reshape(4, 2)
        markers[marker_id] = points

        for corner_index, (u, v) in enumerate(points):
            position = (int(u) + 5, int(v) - 5)

            cv2.putText(
                preview,
                f"{marker_id}:{corner_index}",
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                255,
                2
            )

cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Corners", 1000, 750)
cv2.imshow("Corners", preview)
cv2.waitKey(0)
cv2.destroyAllWindows()