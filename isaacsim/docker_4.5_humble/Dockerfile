# syntax=docker/dockerfile:1.6

ARG ISAAC_VER=4.5.0
FROM nvcr.io/nvidia/isaac-sim:${ISAAC_VER}

# ---------- Root for installs ----------
USER root
ENV DEBIAN_FRONTEND=noninteractive

COPY img_dump/apt_manual.txt /tmp/apt_manual.txt

# Base system + ROS sources
RUN apt-get update && apt-get install -y --no-install-recommends \
    vulkan-tools libvulkan1 mesa-vulkan-drivers lsb-release curl \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
      http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/ros2.list

# ROS and dev tools
RUN apt-get update && \
    sed -e 's/#.*//' -e '/^\s*$/d' /tmp/apt_manual.txt | xargs -r apt-get install -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    build-essential python3-colcon-common-extensions python3-rosdep python3-argcomplete \
    ros-humble-ros-base ros-humble-vision-msgs ros-humble-angles \
    ros-humble-controller-interface ros-humble-joint-trajectory-controller \
    ros-humble-ament-cmake ros-humble-rclpy ros-humble-rcl ros-humble-rcpputils \
    ros-humble-rmw-fastrtps-cpp ros-humble-rmw-fastrtps-shared-cpp ros-humble-rosidl-runtime-cpp \
    ros-humble-ros2-control ros-humble-ros2-controllers \
    ros-humble-controller-manager ros-humble-controller-manager-msgs \
    ros-humble-hardware-interface ros-humble-transmission-interface \
    ros-humble-forward-command-controller ros-humble-joint-state-broadcaster \
    libgl1-mesa-glx libglx0 libglvnd0 libgl1 libegl1 \
    nvidia-cuda-toolkit nvidia-cuda-dev nvidia-opencl-dev \
    git unzip zip wget bash-completion nano vim sudo locales \
    libglvnd-dev libx11-6 libxext6 socat && \
    rm -rf /var/lib/apt/lists/*

# Init rosdep with proper permissions and defaults
RUN rm -rf /etc/ros/rosdep/sources.list.d/20-default.list && \
    rosdep init && \
    rosdep fix-permissions && \
    export ROS_DISTRO=humble && rosdep update

# ---------- Install Python pip deps ----------
COPY pip/requirements_all.txt /tmp/requirements_all.txt
RUN /isaac-sim/python.sh -m pip install --no-cache-dir -r /tmp/requirements_all.txt || true
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --no-cache-dir -r /tmp/requirements_all.txt || true

# ---------- Ensure developer user exists ----------
RUN id -u developer >/dev/null 2>&1 || useradd -m -s /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/developer

# NVIDIA patch
COPY nvidia_glx_patch.tar.gz /tmp/
RUN tar -xzvf /tmp/nvidia_glx_patch.tar.gz -C / && ldconfig

# ---------- Set up workspace with UR driver ----------
USER developer
WORKDIR /workspace

RUN mkdir -p /workspace/ros_ws/src

# Use PickNik's complete and working monorepo for all UR packages
RUN git clone -b humble-devel https://github.com/PickNikRobotics/universal_robot.git /workspace/ros_ws/src/universal_robot || true

# Resolve dependencies
USER root
RUN export ROS_DISTRO=humble && \
    rosdep fix-permissions && rosdep update && \
    rosdep install --from-paths /workspace/ros_ws/src \
        --ignore-src \
        --rosdistro=humble \
        --skip-keys="joint_state_publisher \
        ros2_controllers_test_nodes rviz2 xacro hardware_interface_testing \
        moveit_kinematics moveit_planners_ompl moveit_ros_move_group \
        moveit_ros_visualization moveit_servo moveit_simple_controller_manager \
        warehouse_ros_sqlite \
        ur_client_library ur_msgs joint_state_publisher_gui liburdfdom-tools" \
        -r -y

# Build it using bash for 'source' support
USER developer
RUN bash -c "cd /workspace/ros_ws && source /opt/ros/humble/setup.bash && colcon build --symlink-install"

# ---------- Patch Isaac Sim extensions ----------
USER root
RUN mkdir -p /isaac-sim/extsDeprecated
COPY exts/omni.isaac.core_archive /isaac-sim/exts/omni.isaac.core_archive
COPY exts/omni.isaac.core /isaac-sim/extsDeprecated/omni.isaac.core
COPY exts/omni.isaac.core_nodes /isaac-sim/extsDeprecated/omni.isaac.core_nodes

# ---------- Clean Python cache ----------
RUN find /isaac-sim -name '*.pyc' -delete && find /isaac-sim -name '__pycache__' -exec rm -rf {} +

# ---------- Developer entry ----------
COPY entrypoint.sh /usr/local/bin/ros_entrypoint.sh
RUN chmod +x /usr/local/bin/ros_entrypoint.sh

USER developer
WORKDIR /workspace

# ---------- ENV ----------
ENV ACCEPT_EULA=Y \
    PRIVACY_CONSENT=Y \
    QT_X11_NO_MITSHM=1 \
    __GLX_VENDOR_LIBRARY_NAME=nvidia \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics,display \
    XDG_RUNTIME_DIR=/tmp/runtime-developer \
    ROS_DISTRO=humble \
    ROS_LOCALHOST_ONLY=0 \
    KIT_REPO_NAME=isaac-sim \
    KIT_SAVED_USER_DIR=/home/developer/.nvidia-omniverse \
    KIT_CACHE_DIR=/home/developer/.cache/ov \
    KIT_CONFIG_DIR=/home/developer/.config/ov \
    KIT_USER_DIR=/home/developer/.nvidia-omniverse \
    LD_LIBRARY_PATH=/isaac-sim/kit:$LD_LIBRARY_PATH

ENTRYPOINT ["/usr/local/bin/ros_entrypoint.sh"]
CMD ["/isaac-sim/isaac-sim.sh"] 
