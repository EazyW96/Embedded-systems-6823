# The Frequency Finders: An Autonomous Guided Vehicle

## **Project Overview**
The Frequency Finders is an autonomous guided vehicle (AGV) project developed for the SWE 6823 Embedded Systems class. The system uses a Raspberry Pi, motors, a camera, sensors, and RF modules to detect and navigate to a beacon emitting a specific radio frequency while avoiding obstacles. This repository contains the code, documentation, and resources for the project.

---

## **Features**
- **RF Beacon Detection**: Locate a beacon emitting a specific radio frequency.
- **Obstacle Avoidance**: Navigate around obstacles using sensor data.
- **Autonomous Navigation**: Efficient motor control and navigation algorithms.
- **Real-Time Processing**: Process data from sensors and RF modules in real-time.

---

## **Project Structure**
```
SignalScout/
├── docs/                  # Project documentation
├── src/                   # Source code
│   ├── motor_control.py   # Code for controlling motors
│   ├── rf_detection.py    # RF signal detection logic
│   ├── obstacle_avoid.py  # Obstacle avoidance algorithms
│   └── main.py            # Main program
├── tests/                 # Unit and integration tests
├── diagrams/              # Architecture and data flow diagrams
└── README.md              # Project overview and setup instructions
```

---

## **Getting Started**

### **Hardware Requirements**
- *To be determined.*

### **Software Requirements**
*To be determined.*

### **Setup Instructions**
*To be determined.*

---

## **Project Milestones**
- **Week 1-2**: Team Formation and Presentation of Ideas (Due on Jan 24, 2025, 11:59 PM)
  - Submit a single document listing:
    - Team name.
    - Team members (identify the leader).
    - Three proposed project ideas, each describing:
      - Processes managed by embedded systems.
      - A brief explanation of the idea.

- **Week 3-4**: Project Description and Implementation Plan (Due on Feb 17, 2025, 11:59 PM)
  - Select one of your approved project proposals.
  - Include all processes controlled by embedded systems.
  - Include all processes controlled by embedded systems.

- **Week 5-6**: Project Description, Design, and Implementation Plan (Due on Mar 10, 2025, 11:59 PM)
  - Submit a fully-fleshed out project description.
  - Provide the design and implementation plan.
  - Include hardware requirements and code that will control your system.
  - Submit a fully-fleshed out description of the system.

- **Week 7-8**: Group Project Presentation (Due on Apr 21, 2025, 11:59 PM)
  - Present your group project in a brief video (4 minutes or less).
  - Not all team members need to appear in the video.
  - Include a slide presentation with narration.

 
      

---

## **Contributing**
1. **Fork the Repository**:
   - Go to the repository's GitHub page: [The Frequency Finders Repo](https://github.com/yourusername/TheFrequencyFinders).
   - Click on the "Fork" button in the top-right corner to create your copy of the repository.

2. **Clone the Forked Repository**:
   - Open your terminal and run the following command:
     ```bash
     git clone https://github.com/yourusername/TheFrequencyFinders.git
     ```
   - Replace `yourusername` with your GitHub username.

3. **Create a New Branch**:
   - Navigate to the project directory:
     ```bash
     cd TheFrequencyFinders
     ```
   - Create and switch to a new branch for your feature or bugfix:
     ```bash
     git checkout -b feature-or-bugfix-name
     ```

4. **Make Changes and Commit**:
   - Add your changes and stage them:
     ```bash
     git add .
     ```
   - Commit your changes with a meaningful message:
     ```bash
     git commit -m "Describe your changes here"
     ```

5. **Push Your Branch**:
   - Push your changes to your forked repository:
     ```bash
     git push origin feature-or-bugfix-name
     ```

6. **Submit a Pull Request**:
   - Go to the original repository on GitHub.
   - Click on "Pull Requests" and then "New Pull Request."
   - Select your branch from your forked repository and submit the pull request with detailed comments describing your changes.

---

**Collaboration Tips**:
- Make sure to pull the latest changes from the main repository regularly:
  ```bash
  git pull upstream main
  ```
- Resolve any merge conflicts before pushing your changes.
- Use clear and concise commit messages to describe your work.

## **Contact**
**Team Name**: The Frequency Finders Team  
**Team Lead**: Ryan Hanrahan  
**Team Members**: Vladimir Maximov, Elliotte Wideman  
 
For any queries, contact:  
Ryan Hanrahan: `rhanrah1@students.kennesaw.edu`  
Vladimir Maximov: `vmaximov@students.kennesaw.edu`
Elliotte Wideman: `ewideman@students.kennesaw.edu`
