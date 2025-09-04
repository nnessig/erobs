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
# From the repo root
docker build -t isaac-sim:4.5-humble_ros_ws_fullybuilt ./isaacsim/docker_4.5_humble
```

### Run Isaac Sim
```bash
xhost +local:docker
docker run --rm -it   --runtime=nvidia --gpus all --device /dev/dri:/dev/dri   -v ./isaacsim:/workspace/erobs:rw   -v ./isaacsim/docker_4.5_humble/ros_ws:/workspace/ros_ws:rw   isaac-sim:4.5-humble_ros_ws_fullybuilt     /isaac-sim/isaac-sim.sh     --enable isaacsim.ros2.bridge     /workspace/erobs/erobs-isaacsim.usd
```

---

## Documentation

- [Setup Guide (host installs)](docs/SETUP.md)
- [Docker usage](docs/DOCKER.md)
- [UR3e + ROS 2 integration](docs/ROS2_UR3E.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## License
Distributed under the BSD 3-Clause License. See [LICENSE](../LICENSE) for details.
