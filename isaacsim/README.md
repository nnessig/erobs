# erobs Isaac Sim + ROS 2 Humble Setup

Custom Isaac Sim 4.5 + UR3e + ROS 2 Humble + MoveIt environment, containerized with Docker for reproducibility.  

This repo provides:
- A Docker-based Isaac Sim 4.5 environment
- Integrated ROS 2 Humble with full `ros2_control` and MoveIt
- UR3e robot model + description
- Persistent volume mounts for reproducible development

---

## Quickstart

### Build the Docker image
```bash
# host$ (from the repo root)
docker build -t isaac-sim:4.5-humble_ros_ws_fullybuilt ./isaacsim/docker_4.5_humble
