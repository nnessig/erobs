#!/bin/bash
export NVIDIA_LOG_LEVEL=debug

xhost +local:docker

docker run -it --rm \
  --gpus all \
  --runtime=nvidia \
  --network host \
  --cap-add SYS_ADMIN \
  --security-opt seccomp=unconfined \
  --user $(id -u):$(id -g) \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e ACCEPT_EULA=Y \
  -e PRIVACY_CONSENT=Y \
  -e OMNI_LOG_FILE="/tmp/kit_logs/kit.log" \
  -e ISAAC_PATH=/isaac-sim/exts:/isaac-sim/extsDeprecated \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics,display \
  -e XDG_RUNTIME_DIR=/tmp/runtime-developer \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /tmp/runtime-developer:/tmp/runtime-developer:rw \
  -v ~/Documents/erobs/isaacsim:/isaac-sim:rw \
  -v ~/Documents/erobs/isaacsim/isaac-assets:/isaac-sim/isaac-assets:rw \
  -v ~/Documents/erobs/isaacsim/ros2_ws:/ros2_ws:rw \
  -v ~/Documents/erobs/.nvidia-omniverse:/home/developer/.nvidia-omniverse:rw \
  -v ~/.config/ov:/home/developer/.config/ov:rw \
  isaac-sim:4.5-humble_ros_ws
