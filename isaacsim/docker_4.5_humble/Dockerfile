# Start from official Isaac Sim 4.5 image
FROM nvcr.io/nvidia/isaac-sim:4.5.0

# Install ROS 2 Humble and build tools
USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl gnupg2 lsb-release software-properties-common && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
      http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/ros2.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      ros-humble-ros-base \
      python3-colcon-common-extensions \
      python3-rosdep \
      python3-argcomplete \
      build-essential && \
    rosdep init && rosdep update && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Vulkan loader and GPU drivers inside the container
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libvulkan1 \
      mesa-vulkan-drivers \
      vulkan-tools && \
    rm -rf /var/lib/apt/lists/*

# Create dev workspace and user
RUN mkdir -p /workspace && useradd -ms /bin/bash developer
WORKDIR /workspace
USER developer

# Set up entrypoint to source ROS 2 on launch
COPY --chown=developer:developer entrypoint.sh /workspace/entrypoint.sh
RUN chmod +x /workspace/entrypoint.sh
ENTRYPOINT ["/workspace/entrypoint.sh"]
CMD ["bash"]
