import cv2
import numpy as np
from Camera import Camera


class ArUcoDetector:

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    def __init__(self, dict_to_use):
        self.dict_to_use = dict_to_use

        # Modern OpenCV API
        self.arucoDict = cv2.aruco.getPredefinedDictionary(
            ArUcoDetector.ARUCO_DICT[dict_to_use]
        )

        self.arucoParams = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.arucoDict, self.arucoParams)

    def detect(self, image):
        corners, ids, rejected = self.detector.detectMarkers(image)
        return corners, ids, rejected

    @staticmethod
    def getImageWithMarkers(input_image, detect_res):
        image = input_image.copy()
        corners, ids, rejected = detect_res

        if ids is not None and len(corners) > 0:
            ids = ids.flatten()

            for (markerCorner, markerID) in zip(corners, ids):
                pts = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = pts

                topLeft = tuple(map(int, topLeft))
                topRight = tuple(map(int, topRight))
                bottomRight = tuple(map(int, bottomRight))
                bottomLeft = tuple(map(int, bottomLeft))

                # Draw bounding box
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

                # Draw center
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

                # Draw ID
                cv2.putText(
                    image,
                    str(markerID),
                    (topLeft[0], topLeft[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        return image


if __name__ == '__main__':
    dict_to_use = 'DICT_5X5_50'
    arucoDetector = ArUcoDetector(dict_to_use)

    camera = Camera()
    camera.startStreaming()

    try:
        while True:
            frame = camera.getNextFrame()
            depth_image, color_image = camera.extractImagesFromFrame(frame)

            grey_color = 153
            depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
            masked_color_image = np.where(
                depth_image_3d <= 0, grey_color, color_image
            )

            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.03),
                cv2.COLORMAP_JET
            )

            result = arucoDetector.detect(color_image)

            color_image = ArUcoDetector.getImageWithMarkers(color_image, result)
            masked_color_image = ArUcoDetector.getImageWithMarkers(masked_color_image, result)
            depth_colormap = ArUcoDetector.getImageWithMarkers(depth_colormap, result)

            images = np.hstack((color_image, masked_color_image, depth_colormap))

            cv2.imshow('RealSense', images)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                break

    finally:
        camera.stopStreaming()
        cv2.destroyAllWindows()
