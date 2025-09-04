# Troubleshooting

## GPU/Vulkan mismatch (ERROR_INCOMPATIBLE_DRIVER)
```bash
# host$
# Fix steps
# 1. Upgrade NVIDIA driver to 565
# 2. Install mesa-vulkan-drivers
# 3. Configure NVIDIA Container Toolkit
sudo apt install -y mesa-vulkan-drivers
sudo nvidia-ctk runtime configure --runtime=docker
```

## Missing isaac-sim.sh
```bash
# host$
# Fix: Copy entire /isaac-sim directory from a working container and launch:
/isaac-sim/isaac-sim.sh
```

## MoveIt Setup Assistant freezes / URDF load errors
```bash
# container$
ros2 run xacro xacro /path/to/ur.urdf.xacro ... > /workspace/ros_ws/ur3e_for_msa.urdf
```
Ensure `QT_X11_NO_MITSHM=1` is set and `/tmp/runtime-developer` permissions are correct.
