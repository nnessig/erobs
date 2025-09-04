# UR3e + ROS 2 Integration

The following repos (on `humble` branch) are cloned into the workspace:
- Universal_Robots_ROS2_Description
- Universal_Robots_ROS2_Driver
- Universal_Robots_Client_Library
- ur_msgs

## Example: Launch MoveIt with Fake Hardware
Run inside the **CONTAINER**.

```bash
# container$
source /opt/ros/humble/setup.bash
source /home/developer/ros_ws/install/setup.bash

ros2 launch ur_moveit_config ur_moveit.launch.py   ur_type:=ur3e robot_ip:=fake use_fake_hardware:=true   use_ros2_control:=true prefix:=ur3e_
```
