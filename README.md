# Realsense ArUco Tracking System

This repository provides code and tools to perform ArUco Marker Tracking using Intel's RealSense D435 depth camera. The system is designed to detect and track ArUco markers in real-time, leveraging the capabilities of the RealSense D435 for depth sensing and marker localization.

## Features
- Real-time detection and tracking of ArUco markers.
- Utilizes Intel's RealSense D435 for depth information.
- Efficient and accurate marker localization.
- Supports easy integration with robotics and other AR/VR applications.
- Non-GUI version compatible with headless servers (e.g., Ubuntu Server, Raspberry Pi).

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

## Setup and Marker Generation

### Generate ArUco Marker
1. Use `ArUcoGenerator.py` to generate ArUco markers.
   ```bash
   python RealsenseArUcoTracking/ArUcoGenerator.py
   ```

2. **Modify Marker Properties**:
   Customize the marker configurations by editing the `config.json` file:
   - `dict_to_use`: The type of ArUco dictionary (e.g., `DICT_5X5_50`).
   - `id`: The ID of the marker to be generated.
   - `visualize`: If `true`, displays the generated marker on the screen.
   - `grey_color`: Adjust the grayscale intensity of the marker.

   Example `config.json`:
   ```json
   {
       "dict_to_use": "DICT_5X5_50",
       "id": 1,
       "visualize": true,
       "grey_color": 153
   }
   ```

3. **Run the non-GUI version**:
   - To test the pose detection, use the `AD_test_pose.py` script.
   - Ideal for systems like Linux/Ubuntu server or Raspberry Pi setups.
   ```bash
   python RealsenseArUcoTracking/AD_test_pose.py
   ```

   This feature ensures that the solution is compatible with non-GUI environments.

## Usage
1. Connect the RealSense D435 depth camera to your system.
2. Run the ArUco Tracking software:
   ```bash
   python ArUcoDetector.py
   ```
3. Adjust the camera setup to focus on the area with the ArUco markers.
4. View the real-time tracking results displayed in the output window.

## Folder Structure
- `src/`: Contains the main source code.
- `data/`: Contains sample videos or images for testing.
- `config/`: Contains configuration files for camera settings and marker parameters.
- `RealsenseArUcoTracking/ArUcoGenerator.py`: Script to generate ArUco markers.
- `RealsenseArUcoTracking/config.json`: Configuration file to modify marker properties.

## Contribution
Contributions are welcome! Feel free to submit issues or pull requests in the [GitHub repository](https://github.com/Ayush-Sharma23/Realsense-Aruco).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Author
**Ayush Sharma**

For any queries or feedback, please feel free to reach out.
