# The Frequency Finders: Autonomous Navigation System

## **Project Overview**
The Frequency Finders is an autonomous-guided vehicle (AGV) project developed for the SWE 6823 Embedded Systems class. This project aims to design and implement an autonomous vehicle using the Freenove 4WD Smart Car Kit powered by Raspberry Pi. The system is equipped with a camera, an ultrasonic sensor, and a BLE module to navigate through a living space, avoid obstacles, and locate a BLE beacon emitting a specific radio frequency. The vehicle supports control via mobile devices and computers, enabling exploration of various autonomous movement strategies.

The project demonstrates key principles of sensor integration, data processing, real-time motion control, and decision-making in embedded systems. It serves as an educational platform for building and modifying autonomous systems to solve real-world challenges.

---

## **Features**
- **BLE Beacon Detection**: Locate a beacon emitting a specific BLE signal using the Raspberry Pi’s built-in BLE module and camera-based object recognition.
- **Obstacle Avoidance**: Utilize the HC-SR04 ultrasonic sensor (mounted on a servo) to detect obstacles at multiple angles (30°, 90°, and 150°) and adjust the vehicle's trajectory accordingly.
- **Autonomous Navigation**: Implement real-time navigation algorithms for efficient path planning and movement control based on sensor data.
- **Sensor Fusion & Real-Time Processing**: Combine inputs from the camera, ultrasonic sensor, and BLE module to continuously adapt the vehicle’s path in dynamic environments.
- **Remote Control Support**: Enable control through mobile devices and computers for testing and demonstration purposes.

---

## **Project Structure**
```
SignalScout/                             # Root folder for the project
│
├── README.md                            # Project overview, goals, installation and running instructions
├── LICENSE                              # License file for the project (e.g., MIT, GPL, etc.)
│
├── docs/                                # Documentation folder
│   ├── project_description.md           # Detailed description of the project: objectives, scope, key features
│   ├── design_diagrams.pdf              # Diagrams and schematics: sensor connection diagrams, algorithm flowcharts, etc.
│   ├── development_timeline.md          # Project development timeline with phases and milestones (see Implementation Plan)
│   └── risk_assessment.md               # Risk assessment document: potential issues and mitigation strategies
│
├── src/                                 # Source code folder
│   ├── main.py                          # Main entry point: initializes modules and runs the main control loop
│   ├── config.py                        # Configuration loader: loads and processes settings from configuration files
│   │
│   └── modules/                         # Modules for different functionalities of the system
│       ├── navigation.py                # Navigation logic: path planning, movement control, sensor data integration
│       ├── obstacle_avoidance.py        # Obstacle detection: processes ultrasonic sensor (HC-SR04) data and makes avoidance decisions
│       ├── ble_detection.py             # BLE signal processing: retrieves RSSI, determines beacon direction, adjusts route accordingly
│       ├── sensor_manager.py            # Sensor management: handles camera, ultrasonic sensor, and BLE module; collects and preprocesses sensor data
│       ├── motor_control.py             # Motor control: converts movement commands into motor actions, controls servos, and integrates PID if needed
│       └── utils.py                     # Utility functions: error handling, logging, and other common helper functions
│
├── config/                              # Configuration files folder
│   ├── config.yaml                      # Main configuration file: sensor thresholds, operation modes, camera settings, etc.
│   └── pid_parameters.json              # PID controller parameters (if used): coefficients for P, I, and D
│
├── tests/                               # Unit tests for system components
│   ├── test_navigation.py               # Unit tests for navigation algorithms
│   ├── test_obstacle_avoidance.py       # Unit tests for the obstacle detection module
│   ├── test_ble_detection.py            # Unit tests for BLE detection and signal processing algorithms
│   └── test_motor_control.py            # Unit tests for motor control functionality
│
├── scripts/                             # Auxiliary scripts and utilities
│   ├── deploy.sh                        # Deployment script: automates environment setup, file copying, and project deployment on target device (e.g., Raspberry Pi)
│   └── battery_monitor.py               # Battery monitoring script: monitors battery status and logs power consumption data
│
├── hardware/                            # Hardware-related documentation and files
│   ├── wiring_diagram.pdf               # Wiring diagram: shows connections between Raspberry Pi, Freenove kit, sensors, and motors
│   └── component_specs.md               # Hardware component specifications: technical details and connection information
│
└── logs/                                # Log files generated during system operation (created dynamically at runtime)
    └── README.md                        # Description of the logging system: what is logged, log file formats, and storage locations
```

---

## **Getting Started**

### **Hardware Requirements**
- Freenove 4WD Smart Car Kit
- Raspberry Pi 3 Model B and/or Raspberry Pi 5
- Raspberry Pi Camera Module
- HC-SR04 Ultrasonic Sensor (mounted on a servo)
- 18650 Rechargeable Batteries (providing 7.4V)
- BLE Beacon (or BLE-capable devices such as smartwatches or headphones)

### **Software Requirements**
- Raspberry Pi OS (or an alternative such as ROS in future iterations)
- Python 3.x
- OpenCV (for image processing and object recognition)
- Additional Python libraries as specified in the project’s configuration files

### **Setup Instructions**
*To be determined:* Detailed instructions for hardware assembly, software installation, and initial configuration will be provided in the documentation and setup guides.


---

## **Project Milestones**
- **Week 1-2**: Team Formation and Idea Presentation (Due on Jan 24, 2025, 11:59 PM)
  - Submit a document listing team name, team members (with the leader identified), and three proposed project ideas, each outlining:
    - Embedded systems processes managed by the project.
    - A brief explanation of each idea.

- **Week 3-4**: Project Description and Implementation Plan (Due on Feb 17, 2025, 11:59 PM)
  - Select one approved project proposal.
  - Include all embedded systems processes, hardware requirements, and a high-level plan for the system’s control.

- **Week 5-6**: Detailed Project Description, Design, and Implementation Plan (Due on Mar 10, 2025, 11:59 PM)
  - Submit a fully detailed project description.
  - Provide comprehensive design diagrams and an implementation plan.
  - Include hardware requirements and initial code outlines.

- **Week 7-8**: Group Project Presentation (Due on Apr 21, 2025, 11:59 PM)
  - Present the project in a brief video (4 minutes or less).
  - Not all team members need to appear, but include a slide presentation with narration.

---

## **Contributing**

1. **Fork the Repository**:
   - Go to the repository’s GitHub page: [The Frequency Finders Repo](https://github.com/yourusername/TheFrequencyFinders).
   - Click the "Fork" button to create your own copy of the repository.

2. **Clone the Forked Repository**:
   - Open your terminal and run:
     ```bash
     git clone https://github.com/yourusername/TheFrequencyFinders.git
     ```
   - Replace `yourusername` with your GitHub username.

3. **Create a New Branch**:
   - Navigate to the project directory:
     ```bash
     cd TheFrequencyFinders
     ```
   - Create and switch to a new branch:
     ```bash
     git checkout -b feature-or-bugfix-name
     ```

4. **Make Changes and Commit**:
   - Stage your changes:
     ```bash
     git add .
     ```
   - Commit with a descriptive message:
     ```bash
     git commit -m "Describe your changes here"
     ```

5. **Push Your Branch**:
   - Push the changes:
     ```bash
     git push origin feature-or-bugfix-name
     ```

6. **Submit a Pull Request**:
   - On GitHub, navigate to "Pull Requests" and click "New Pull Request."
   - Select your branch and submit the pull request with detailed comments.

**Collaboration Tips**:
- Make sure to pull the latest changes from the main repository regularly:
  ```bash
  git pull upstream main
  ```
- Resolve any merge conflicts before pushing your changes.
- Use clear and concise commit messages to describe your work.

---

## **Contact**
**Team Name**: The Frequency Finders Team  
**Team Lead**: Ryan Hanrahan  
**Team Members**: Vladimir Maximov, Elliotte Wideman  
 
For any queries, contact:  
- Ryan Hanrahan: `rhanrah1@students.kennesaw.edu`  
- Vladimir Maximov: `vmaximov@students.kennesaw.edu` 
- Elliotte Wideman: `ewideman@students.kennesaw.edu` 
- Tyler Breedlove: `tbreedl1@students.kennesaw.edu`