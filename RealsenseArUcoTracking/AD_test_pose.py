import cv2
import numpy as np
import pyrealsense2 as rs
from Camera import Camera


class ArUcoDetector:

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50
    }

    def __init__(self, dict_to_use):
        self.dict_to_use = dict_to_use

        self.arucoDict = cv2.aruco.getPredefinedDictionary(
            ArUcoDetector.ARUCO_DICT[dict_to_use]
        )

        self.arucoParams = cv2.aruco.DetectorParameters()

        self.detector = cv2.aruco.ArucoDetector(
            self.arucoDict,
            self.arucoParams
        )

    def detect(self, image):
        corners, ids, rejected = self.detector.detectMarkers(image)
        return corners, ids, rejected

    def estimate_pose(self, corners, marker_length, camera_matrix, dist_coeffs):
        rvecs = []
        tvecs = []

        half_size = marker_length / 2.0

        # 3D coordinates of marker corners
        obj_points = np.array([
            [-half_size,  half_size, 0],
            [ half_size,  half_size, 0],
            [ half_size, -half_size, 0],
            [-half_size, -half_size, 0]
        ], dtype=np.float32)

        for corner in corners:
            img_points = corner.reshape((4, 2)).astype(np.float32)

            success, rvec, tvec = cv2.solvePnP(
                obj_points,
                img_points,
                camera_matrix,
                dist_coeffs
            )

            if success:
                rvecs.append(rvec)
                tvecs.append(tvec)

        return rvecs, tvecs

    @staticmethod
    def draw_markers(image, corners, ids):
        if ids is None:
            return image

        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            pts = markerCorner.reshape((4, 2))
            (tl, tr, br, bl) = pts

            tl = tuple(map(int, tl))
            tr = tuple(map(int, tr))
            br = tuple(map(int, br))
            bl = tuple(map(int, bl))

            # Draw bounding box
            cv2.line(image, tl, tr, (0, 255, 0), 2)
            cv2.line(image, tr, br, (0, 255, 0), 2)
            cv2.line(image, br, bl, (0, 255, 0), 2)
            cv2.line(image, bl, tl, (0, 255, 0), 2)

            # Center point
            cX = int((tl[0] + br[0]) / 2.0)
            cY = int((tl[1] + br[1]) / 2.0)

            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

            # ID text
            cv2.putText(
                image,
                str(markerID),
                (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return image


def get_realsense_intrinsics(camera):
    profile = camera.pipeline.get_active_profile()
    stream = profile.get_stream(rs.stream.color)
    intrinsics = stream.as_video_stream_profile().get_intrinsics()

    camera_matrix = np.array([
        [intrinsics.fx, 0, intrinsics.ppx],
        [0, intrinsics.fy, intrinsics.ppy],
        [0, 0, 1]
    ])

    dist_coeffs = np.array(intrinsics.coeffs)

    return camera_matrix, dist_coeffs


# ========================= MAIN =========================

if __name__ == "__main__":

    dict_to_use = "DICT_5X5_50"
    marker_length = 0.05  # meters (IMPORTANT: set real marker size)

    arucoDetector = ArUcoDetector(dict_to_use)

    camera = Camera()
    camera.startStreaming()

    camera_matrix, dist_coeffs = get_realsense_intrinsics(camera)

    print("[INFO] Camera matrix:\n", camera_matrix)
    print("[INFO] Distortion:\n", dist_coeffs)

    try:
        while True:
            frame = camera.getNextFrame()
            depth_image, color_image = camera.extractImagesFromFrame(frame)

            corners, ids, rejected = arucoDetector.detect(color_image)

            output = ArUcoDetector.draw_markers(color_image.copy(), corners, ids)

            if ids is not None and len(corners) > 0:

                rvecs, tvecs = arucoDetector.estimate_pose(
                    corners,
                    marker_length,
                    camera_matrix,
                    dist_coeffs
                )

                for i in range(len(tvecs)):
                    tvec = tvecs[i].flatten()
                    rvec = rvecs[i]

                    x, y, z = tvec

                    print(f"[POSE] ID {ids[i][0]} → X: {x:.3f} m | Y: {y:.3f} m | Z: {z:.3f} m")

                    # Draw coordinate axes
                    cv2.drawFrameAxes(
                        output,
                        camera_matrix,
                        dist_coeffs,
                        rvec,
                        tvec,
                        0.03
                    )

            cv2.imshow("ArUco Pose Estimation", output)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        camera.stopStreaming()
        cv2.destroyAllWindows()
