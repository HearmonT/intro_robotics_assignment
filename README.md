# ROS 2 Robotics Assignment: Custom Interfaces & Navigation

This repository contains a ROS 2 (Humble/Iron) workspace implementation featuring custom message, service, and action interfaces, obstacle avoidance service toggles, and a custom action server for autonomous distance navigation.

## Repository Structure

```text
intro_robotics_assignment/
├── src/
│   ├── my_robot_interfaces/   # Custom ROS 2 messages, services, and action definitions
│   └── my_robot_nodes/        # Core execution nodes (obstacle avoidance & action server)

```

## Packages Included

1. **`my_robot_interfaces`**:
* **`RobotStatus.msg`**: Custom message for publishing robot operational states.
* **`SetTurnSpeed.srv`**: Service definition for dynamically modifying turn velocity.
* **`NavigateDistance.action`**: Custom action interface defining target distance and live feedback.


2. **`my_robot_nodes`**:
* **`turn_away.py`**: Obstacle avoidance node with a service toggle (`/turn_away_enable`).
* **`navigate_distance_server.py`**: Action server node handling goal requests, streaming live distance feedback, and executing smooth stops upon completion.



---

## How to Build and Run

### 1. Clone and Build Workspace

```bash
cd ~
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone [https://github.com/HearmonT/intro_robotics_assignment.git](https://github.com/HearmonT/intro_robotics_assignment.git) .
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install

```

### 2. Source the Environment

```bash
source ~/ros2_ws/install/setup.bash

```

### 3. Run the Action Server

```bash
ros2 run my_robot_nodes navigate_distance_server

```

### 4. Send an Action Goal (CLI Example)

Open a new terminal, source your workspace, and send a navigation goal:

```bash
source ~/ros2_ws/install/setup.bash
ros2 action send_goal /navigate_distance my_robot_interfaces/action/NavigateDistance "{target_distance: 2.0, speed: 0.2}"

```

```

```
