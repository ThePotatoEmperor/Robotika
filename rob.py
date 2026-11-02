from ctu_crs import CRS97
import cv2

robot = CRS97()
robot.initialize()

try:
    # First capture initializes the camera
    img = robot.grab_image()

    if img is None:
        raise RuntimeError("Could not capture an image.")

    # Access the initialized Basler camera
    camera = robot._camera

    # Disable auto exposure
    camera.camera.ExposureAuto.SetValue("Off")

    # Set exposure to 2 ms (2000 microseconds)
    camera.camera.ExposureTime.SetValue(2000.0)

    print(
        "Exposure:",
        camera.camera.ExposureTime.GetValue(),
        "µs"
    )

    # Capture image with new exposure
    img = robot.grab_image()

    # Continue with your existing OpenCV and ArUco code...


    if img is None:
        raise RuntimeError("Could not capture an image.")

    # Show original camera image
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 800, 600)
    cv2.imshow("Camera", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Copy image for marker visualization
    preview = img.copy()

    # ArUco marker dictionary
    dictionary = cv2.aruco.getPredefinedDictionary(
        cv2.aruco.DICT_4X4_1000
    )

    detector = cv2.aruco.ArucoDetector(dictionary)

    # Detect markers
    corners, ids, _ = detector.detectMarkers(img)

    markers = {}

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(preview, corners, ids)

        for marker_corners, marker_id in zip(
            corners, ids.flatten()
        ):
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

        print(f"Detected {len(markers)} markers")
    else:
        print("No ArUco markers detected.")

    # Show detected corners
    cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Corners", 1000, 750)
    cv2.imshow("Corners", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




finally:
    cv2.destroyAllWindows()
    robot.close()
