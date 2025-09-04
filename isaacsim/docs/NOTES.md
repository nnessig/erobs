# Additional Notes and References

This file collects detailed context, workarounds, and background notes from the original full setup guide
that were not included in the streamlined README, SETUP, DOCKER, ROS2_UR3E, and TROUBLESHOOTING documents.

---

## Project Structure (Detailed)

```text
~/Documents/erobs/isaacsim
├── docker_4.5_humble/          # Docker context and ROS 2 workspace
│   ├── Dockerfile
│   ├── ros_ws/                  # colcon workspace
│   │   ├── src/
│   │   ├── build/
│   │   ├── install/
│   │   └── log/
│   └── scripts/                 # helper scripts
├── assets/                      # USD assets, textures, models
├── scripts/                     # launch helpers
├── erobs-isaacsim.usd           # main USD stage
└── README.md                    # top-level readme
```

Inside Docker container:

```text
/isaac-sim
/workspace/erobs                 # bind-mounted USD_DIR
/workspace/ros_ws                # bind-mounted ROS workspace
/home/developer/.cache/ov        # Omniverse cache
/home/developer/.cache/pip       # pip cache
/home/developer/.local/share/ov/data  # Omniverse data
```

---

## Environment & Setup Issues

### Docker + GPU
- Encountered CUDA and Vulkan errors launching Isaac Sim inside Docker (`VkResult: ERROR_INCOMPATIBLE_DRIVER`, CUDA context creation failures).
- Required proper NVIDIA Container Toolkit setup with `--runtime=nvidia`, `--gpus all`, and device cgroup rules.
- Often fixed by ensuring correct Vulkan ICD drivers were mounted.

### Volume Mounts & File Paths
- Confusion between host, root, and developer paths.
- Resolved by standardizing volume mounting for:
  - ROS 2 workspace (`ros_ws`)
  - Isaac Sim caches and data
  - Custom asset directory (`isaac-assets`)

### UR3e Robot Integration
- **URDF / XACRO**: Some URDFs that worked in RViz crashed MoveIt Setup Assistant. Required flattening XACRO to plain URDF before loading.
- **Articulation Root**: Robot did not move until articulation root was placed on `base_link_inertia` instead of top-level prim. Nested roots or missing PhysxRigidBodyAPI caused errors.

### ROS 2 Integration
- Only `isaacsim.ros2.bridge` extension was available (not `omni.isaac.ros2_bridge`).
- No Isaac Sim GUI integration for ROS 2 controllers in 4.5 — all controller work is CLI-based.

### MoveIt and Controller Setup
- **MoveIt Setup Assistant (MSA)**: Froze or crashed when loading certain URDFs. Often caused by X11 UID mismatch in `/tmp/runtime-developer`.
- **UR Controllers Build Errors**: `ur_controllers` initially failed until moved to top-level `src/` directory. Required minor code patches.

### Package Management & Dependencies
- Had to manually clone repos that were missing from base Isaac Sim + ROS 2 container:
  - Universal_Robots_ROS2_Description
  - Universal_Robots_ROS2_Driver
  - Universal_Robots_Client_Library
  - ur_controllers (patched and relocated)
- An accidental `sudo apt autoremove` removed key ROS/Gazebo/RViz packages, which had to be reinstalled.

---

## MoveIt Setup Assistant (Detailed Notes)

- Flatten XACRO to URDF before loading into MSA:
  ```bash
  # container$
  ros2 run xacro xacro ur.urdf.xacro ... > ur3e_for_msa.urdf
  ```
- Patched ros2_control hardware plugin block to use fake hardware for compatibility.
- Generated configs from MSA (controllers.yaml, SRDF, etc.) were partially usable but required manual cleanup.

---

## URDF / XACRO Details

- UR3e URDF generated using `ur.urdf.xacro` from Universal_Robots_ROS2_Description repo.
- Included full `ros2_control` block using `ur_robot_driver/URPositionHardwareInterface` plugin.
- Namespaces and prefixes must match between URDF and controllers or load failures occur.

---

## Known Workarounds Summary

- **GPU/Vulkan mismatch** → Upgrade to NVIDIA driver 565, install mesa-vulkan-drivers, configure container toolkit.
- **Missing isaac-sim.sh** → Copy `/isaac-sim` directory from working container.
- **ros2_control GUI absent** → Use CLI (`ros2 control list_controllers`, `ros2 control load_start_controller ...`).
- **UR controllers CMake errors** → Move `ur_controllers` package to top-level `src/` and patch functions.
- **MSA freeze** → Ensure `/tmp/runtime-developer` permissions and UID alignment, flatten URDF before loading.

---

## Package List Reminder

Installed via apt in container and/or host:

- `ros-humble-desktop`
- `ros-humble-moveit`
- `ros-humble-ros2-control`
- `ros-humble-ros2-controllers`
- `ros-humble-ur-client-library`
- `ros-humble-rviz2`
- `ros-humble-gazebo-ros2-control`
- `python3-colcon-common-extensions`
- `python3-vcstool`
- `python3-rosdep`

---

End of Notes.
