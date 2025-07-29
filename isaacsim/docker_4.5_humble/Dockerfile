# syntax=docker/dockerfile:1.6

ARG ISAAC_VER=4.5.0
FROM nvcr.io/nvidia/isaac-sim:${ISAAC_VER}

# ---------- Root for installs ----------
USER root
ENV DEBIAN_FRONTEND=noninteractive

COPY img_dump/apt_manual.txt /tmp/apt_manual.txt

# Base system + ROS sources
RUN apt-get update && \
    apt-get install -y --no-install-recommends --allow-downgrades libbrotli1=1.0.9-2build6 && \
    apt-mark hold libbrotli1 && \
    apt-get install -y --no-install-recommends \
        vulkan-tools libvulkan1 mesa-vulkan-drivers lsb-release curl && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
      http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/ros2.list

# ROS and dev tools
RUN apt-get update && \
    sed -e 's/#.*//' -e '/^\s*$/d' /tmp/apt_manual.txt | \
      xargs -r apt-get install -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
        build-essential python3-colcon-common-extensions python3-rosdep python3-argcomplete \
        python3-ament-package python3-empy \
        ros-humble-ros-base ros-humble-vision-msgs ros-humble-angles \
        ros-humble-controller-interface ros-humble-joint-trajectory-controller \
        ros-humble-controller-manager ros-humble-controller-manager-msgs \
        ros-humble-ros2-control ros-humble-ros2-controllers \
        ros-humble-ros2-control-test-assets \
        ros-humble-ros2-controllers-test-nodes \
        ros-humble-hardware-interface-testing \
        ros-humble-warehouse-ros-sqlite \
        liburdfdom-tools \
        ros-humble-pluginlib \
        ros-humble-rcutils \
        ros-humble-realtime-tools \
        ros-humble-generate-parameter-library \
        ros-humble-lifecycle-msgs \
        ros-humble-trajectory-msgs \
        ros-humble-control-msgs \
        ros-humble-action-msgs \
        ros-humble-ament-cmake ros-humble-ament-cmake-gmock ros-humble-ament-cmake-google-benchmark \
        ros-humble-rclpy ros-humble-rcl ros-humble-rcpputils \
        ros-humble-rmw-fastrtps-cpp ros-humble-rmw-fastrtps-shared-cpp ros-humble-rosidl-runtime-cpp \
        ros-humble-hardware-interface ros-humble-transmission-interface \
        ros-humble-forward-command-controller ros-humble-joint-state-broadcaster \
        ros-humble-moveit \
        ros-humble-moveit-ros-move-group \
        ros-humble-moveit-ros-visualization \
        ros-humble-moveit-ros-planning \
        ros-humble-moveit-planners-ompl \
        ros-humble-moveit-servo \
        ros-humble-moveit-simple-controller-manager \
        ros-humble-moveit-setup-assistant \
        ros-humble-moveit-setup-framework \
        ros-humble-moveit-setup-app-plugins \
        ros-humble-moveit-setup-core-plugins \
        ros-humble-moveit-setup-srdf-plugins \
        ros-humble-moveit-setup-controllers \
        qtbase5-dev qtbase5-dev-tools qttools5-dev qttools5-dev-tools \
        ros-humble-rviz2 \
        ros-humble-robot-state-publisher \
        ros-humble-joint-state-publisher \
        ros-humble-joint-state-publisher-gui \
        ros-humble-tf2-tools ros-humble-tf2-ros ros-humble-tf2-msgs ros-humble-tf2-eigen \
        ros-humble-xacro \
        libfreetype6-dev \
        libgl1-mesa-glx libegl1 libglx0 libglvnd0 \
        libogre1.12.10 libogre-1.12-dev \
        libfreeimage3 libglew2.2 \
        mesa-utils \
        x11-utils \
        libnvidia-gl-565-server \
        libnvidia-common-565-server \
        libnvidia-egl-wayland1 \
        nvidia-cuda-toolkit nvidia-cuda-dev nvidia-opencl-dev \
        git unzip zip wget bash-completion nano vim sudo locales \
        libglvnd-dev libx11-6 libxext6 socat \
        libbackward-cpp-dev && \
    ln -sf /opt/ros/humble/lib/moveit_setup_assistant/moveit_setup_assistant \
           /opt/ros/humble/bin/moveit_setup_assistant && \
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

# ---------- Set up ROS2 workspace with UR packages ----------
USER developer
WORKDIR /workspace/ros_ws/src

# clone UR msgs + driver, description & client repos
RUN git clone -b humble https://github.com/ros-industrial/ur_msgs.git && \
    git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git && \
    git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git && \
    git clone -b master https://github.com/UniversalRobots/Universal_Robots_Client_Library.git

# patch ur_controllers to pull in controller_manager & test_assets
RUN sed -i '/find_package(controller_interface REQUIRED)/a \
    find_package(controller_manager REQUIRED)\n\
    find_package(ros2_control_test_assets REQUIRED)' \
        Universal_Robots_ROS2_Driver/ur_controllers/CMakeLists.txt && \
    sed -i '/set(THIS_PACKAGE_INCLUDE_DEPENDS/a \
    controller_manager\n    ros2_control_test_assets' \
        Universal_Robots_ROS2_Driver/ur_controllers/CMakeLists.txt && \
    sed -i '/<depend>controller_interface<\/depend>/a \
    <depend>controller_manager</depend>\n\
    <depend>ros2_control_test_assets</depend>' \
        Universal_Robots_ROS2_Driver/ur_controllers/package.xml

# flatten so colcon can see everything (including ur3e_bringup & rviz launch)
RUN mv Universal_Robots_ROS2_Driver/* . && rm -rf Universal_Robots_ROS2_Driver && \
    mv Universal_Robots_ROS2_Description/* . && rm -rf Universal_Robots_ROS2_Description

# Add local ur3e_bringup with RViz launch file
COPY ros_ws/src/ur3e_bringup /workspace/ros_ws/src/ur3e_bringup

# install any missing rosdeps
USER root
RUN export ROS_DISTRO=humble && \
    rosdep fix-permissions && \
    rosdep update && \
    rosdep install \
      --from-paths /workspace/ros_ws/src \
      --ignore-src \
      -r -y

# build the entire overlay
USER developer
WORKDIR /workspace/ros_ws

# force bash so that `source setup.bash` works
RUN /bin/bash -lc "\
    source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF\
"

# Link it so ~/ros_ws/install/setup.bash exists
RUN ln -s /workspace/ros_ws /home/developer/ros_ws

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
    LD_LIBRARY_PATH=/isaac-sim/kit:$LD_LIBRARY_PATH \
    PATH="/opt/ros/humble/bin:${PATH}"

ENTRYPOINT ["/usr/local/bin/ros_entrypoint.sh"]
CMD ["/isaac-sim/isaac-sim.sh"]
