# Vehicle-Speed-Detection-System# Vehicle Speed Monitoring System Using OpenCV and Python

## 1. Project Overview
This project aims to develop a vehicle speed monitoring system using computer vision techniques. The system will utilize an IP camera to capture video footage of vehicles within a plant and use Python with OpenCV to detect and track vehicles, calculate their speed, and flag those exceeding the 10 mph speed limit.

## 2. Objectives
- Monitor vehicle speeds in real-time using video analytics.
- Detect and log speed violations.
- Provide a scalable and cost-effective solution using open-source tools.

## 3. Scope
### In Scope:
- Real-time video processing using OpenCV.
- Vehicle detection using YOLOv8 or similar models.
- Speed calculation based on frame analysis and known distances.
- Logging and alerting for speed violations.

### Out of Scope:
- License plate recognition.
- Integration with external databases or security systems.

## 4. Requirements

### 4.1 Hardware Requirements
- IP Camera with:
  - Resolution: 1080p or higher
  - Frame Rate: 30 fps or more
  - Varifocal lens
  - IR night vision (if low-light monitoring is needed)
- Laptop or workstation capable of running Python and OpenCV.

### 4.2 Software Requirements
- Python 3.x
- OpenCV
- NumPy, Pandas
- YOLOv8 (via Ultralytics)
- DeepSORT for tracking
- RTSP stream access from the camera

## 5. System Architecture

### 5.1 Components
- **Camera Module**: Captures video stream.
- **Processing Module**: Python script using OpenCV to detect and track vehicles.
- **Speed Calculation Module**: Computes speed based on time and distance.
- **Alert Module**: Logs and flags vehicles exceeding speed limit.

### 5.2 Data Flow
1. Camera captures video stream.
2. OpenCV reads frames from the stream.
3. YOLOv8 detects vehicles.
4. DeepSORT tracks vehicles across frames.
5. Speed is calculated using frame timestamps and known distances.
6. Violations are logged.

## 6. Development Timeline

| Phase                  | Duration       | Description                          |
|------------------------|----------------|--------------------------------------|
| Requirements Gathering | 1 week         | Finalize specs and hardware options  |
| Research & Setup       | 1 week         | Camera selection and environment setup |
| Development            | 2 weeks        | Implement detection and tracking     |
| Testing & Calibration  | 1 week         | Validate speed calculations          |
| Deployment             | 1 week         | Install and monitor in production    |

## 7. Risk Management

| Risk                          | Mitigation Strategy                          |
|-------------------------------|-----------------------------------------------|
| Inaccurate speed detection    | Calibrate with known distances and test cases |
| Hardware compatibility issues | Research and test with sample streams         |
| Environmental interference    | Use IR cameras and proper mounting            |
| Limited processing power      | Optimize code and use efficient models        |

## 8. Conclusion
This project will provide a reliable and efficient solution for monitoring vehicle speeds within the plant using modern computer vision techniques. With proper calibration and setup, it will enhance safety and compliance with speed regulations.

---

**Prepared by:** Junesh Gautam  
**Date:** July 09, 2025
