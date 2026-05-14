# Realsense ArUco Tracking System

This repository provides code and tools to perform ArUco Marker Tracking using Intel's RealSense D435 depth camera. The system is designed to detect and track ArUco markers in real-time, leveraging the capabilities of the RealSense D435 for depth sensing and marker localization.

## Features
- Real-time detection and tracking of ArUco markers.
- Utilizes Intel's RealSense D435 for depth information.
- Efficient and accurate marker localization.
- Supports easy integration with robotics and other AR/VR applications.

## Prerequisites
- **Hardware:** Intel RealSense D435 Depth Camera.
- **Software:**
  - Python 3.x
  - OpenCV with ArUco module.
  - Intel RealSense SDK 2.0.
- **Platforms:** Supports Linux, Windows, and macOS.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ayush-Sharma23/Realsense-Aruco.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Realsense-Aruco/RealsenseArUcoTracking
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Connect the RealSense D435 depth camera to your system.
2. Run the ArUco Tracking software:
   ```bash
   python aruco_tracking.py
   ```
3. Adjust the camera setup to focus on the area with the ArUco markers.
4. View the real-time tracking results displayed in the output window.

## Folder Structure
- `src/`: Contains the main source code.
- `data/`: Contains sample videos or images for testing.
- `config/`: Contains configuration files for camera settings and marker parameters.

## Contribution
Contributions are welcome! Feel free to submit issues or pull requests in the [GitHub repository](https://github.com/Ayush-Sharma23/Realsense-Aruco).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Author
**Ayush Sharma**

For any queries or feedback, please feel free to reach out.