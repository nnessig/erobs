# syntax=docker/dockerfile:1.6

ARG ISAAC_VER=4.5.0
FROM nvcr.io/nvidia/isaac-sim:${ISAAC_VER}

# ---------- Root for installs ----------
USER root
ENV DEBIAN_FRONTEND=noninteractive

COPY img_dump/apt_manual.txt /tmp/apt_manual.txt

# Base tooling to add ROS repo & generally useful utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    vulkan-tools \
    libvulkan1 \
    mesa-vulkan-drivers \
    && rm -rf /var/lib/apt/lists/*

# ---------------- ROS 2 Humble repo ----------------
RUN apt-get update && apt-get install -y --no-install-recommends lsb-release && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
      http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/ros2.list

# ---------- Install required packages ----------
RUN apt-get update && \
    sed -e 's/#.*//' -e '/^\s*$/d' /tmp/apt_manual.txt | xargs -r apt-get install -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete \
    ros-humble-ros-base \
    ros-humble-vision-msgs \
    ros-humble-angles \
    ros-humble-controller-interface \
    ros-humble-joint-trajectory-controller \
    ros-humble-ament-cmake \
    ros-humble-rclpy ros-humble-rcl ros-humble-rcpputils \
    ros-humble-rmw-fastrtps-cpp ros-humble-rmw-fastrtps-shared-cpp \
    ros-humble-rosidl-runtime-cpp \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-controller-manager \
    ros-humble-controller-manager-msgs \
    ros-humble-hardware-interface \
    ros-humble-transmission-interface \
    ros-humble-forward-command-controller \
    ros-humble-joint-state-broadcaster \
    libgl1-mesa-glx libglx0 libglvnd0 libgl1 libegl1 \
    nvidia-cuda-toolkit nvidia-cuda-dev nvidia-opencl-dev \
    git unzip zip wget bash-completion nano vim sudo locales \
    libglvnd-dev libx11-6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ROS dep init
RUN rosdep init || true && rosdep update || true

# ---------- PIP packages from old image ----------
COPY pip/requirements_all.txt /tmp/requirements_all.txt
RUN /isaac-sim/python.sh -m pip install --no-cache-dir -r /tmp/requirements_all.txt || true
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --no-cache-dir -r /tmp/requirements_all.txt || true

# ---------- Prepare runtime env ----------
RUN mkdir -p /tmp/runtime-developer && chmod 777 /tmp/runtime-developer

# ---------- Patch Isaac Sim extensions ----------
RUN mkdir -p /isaac-sim/extsDeprecated
COPY exts/omni.isaac.core_archive /isaac-sim/exts/omni.isaac.core_archive
COPY exts/omni.isaac.core /isaac-sim/extsDeprecated/omni.isaac.core
COPY exts/omni.isaac.core_nodes /isaac-sim/extsDeprecated/omni.isaac.core_nodes

# ---------- Clean bad Python cache ----------
RUN rm -rf /isaac-sim/exts/*/__pycache__ \
    /isaac-sim/kit/extsPhysics/*/__pycache__ \
    /isaac-sim/kit/exts/*/__pycache__ \
    && find /isaac-sim -name '*.pyc' -delete

# ---------- Entry script ----------
COPY entrypoint.sh /usr/local/bin/ros_entrypoint.sh
RUN chmod +x /usr/local/bin/ros_entrypoint.sh

# ---------- Ensure developer user exists ----------
RUN id -u developer >/dev/null 2>&1 || useradd -m -s /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/developer

# ---------- Developer defaults ----------
COPY nvidia_glx_patch.tar.gz /tmp/
RUN tar -xzvf /tmp/nvidia_glx_patch.tar.gz -C / && \
    ldconfig

USER developer
WORKDIR /workspace

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

