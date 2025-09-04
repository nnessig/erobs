# Host Setup Guide

## 1) System and NVIDIA Drivers
Run on the **HOST**.

```bash
# host$
sudo apt update && sudo apt upgrade -y
sudo apt install -y nvidia-driver-565 nvidia-dkms-565 nvidia-utils-565 ...
nvidia-smi
```

## 2) NVIDIA Container Toolkit
```bash
# host$
sudo apt install -y nvidia-container-toolkit nvidia-container-toolkit-base
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## 3) ROS 2 Repository and Keys
```bash
# host$
sudo apt install -y curl gnupg2 lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null
```

## 4) ROS 2 Packages
```bash
# host$
sudo apt install -y ros-humble-desktop ros-humble-moveit ...
```

## 5) Python Tools
```bash
# host$
python3 -m pip install --upgrade pip setuptools wheel
pip install rospkg catkin_pkg vcstool xacro empy
```

## 6) Directories
```bash
# host$
mkdir -p ./isaacsim/docker_4.5_humble/ros_ws/src
mkdir -p ./docker/isaac-sim/cache/{kit,ov,pip,glcache,computecache,warp}
mkdir -p ./docker/isaac-sim/{logs,data}
```
