# Docker Build and Usage

## Build the Docker Image
Run on the **HOST**.

```bash
# host$
docker build -t isaac-sim:4.5-humble_ros_ws_fullybuilt ./isaacsim/docker_4.5_humble
```

## Run Isaac Sim
```bash
# host$
xhost +local:docker
docker run --rm -it   --runtime=nvidia --gpus all --device /dev/dri:/dev/dri   --cap-add SYS_ADMIN --security-opt seccomp=unconfined   --network host --tmpfs /dev/shm:rw,nosuid,nodev,exec,size=2g   -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1   -v ./isaacsim:/workspace/erobs:rw   -v ./isaacsim/docker_4.5_humble/ros_ws:/workspace/ros_ws:rw   isaac-sim:4.5-humble_ros_ws_fullybuilt     /isaac-sim/isaac-sim.sh     --enable isaacsim.ros2.bridge     /workspace/erobs/erobs-isaacsim.usd
```

## Open a Container Shell
```bash
# host$
docker ps
docker exec -it <ID_or_NAME> bash
```

## Launch RViz2 (inside container)
```bash
# container$
source /opt/ros/humble/setup.bash
source /home/developer/ros_ws/install/setup.bash
ros2 launch ur3e_bringup rviz_ur3e.launch.py
```
