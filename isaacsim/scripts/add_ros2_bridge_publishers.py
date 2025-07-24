"""
add_ros2_bridge_publishers.py

This script programmatically adds a ROS 2 Bridge, TF publisher, and JointState publisher
to an Isaac Sim 4.5 scene via Python API. It is intended to be used when importing
robot models (e.g. UR3e) and connecting them to a ROS 2 system outside the simulator.

What this script sets up:
  - /World/ROS2Bridge (IsaacSimROS2Bridge)
  - /World/ROS2Bridge/TFPublisher → Publishes /tf from /World/ur3e/base_link
  - /World/ROS2Bridge/JointStatePublisher → Publishes /joint_states from /World/ur3e

Usage:
1. Place this script in your mounted workspace (e.g. `/workspace/erobs/scripts/`).
2. Open Isaac Sim and load your robot scene (e.g., with a UR3e in `/World/ur3e`).
3. Run this script (make sure that its path is mounted in Docker):
   - In Script Editor: load & run
   - Or in terminal: `exec(open("/workspace/scripts/add_ros2_bridge_publishers.py").read())` 
4. After confirming it works (via `ros2 topic list`), **SAVE** your stage so it's persistent.

Prerequisites:
- Isaac Sim 4.5+
- ROS 2 Humble workspace with bridge connected
- UR3e or equivalent robot placed under `/World/ur3e`
"""

from omni.isaac.core.utils.prims import create_prim
from pxr import Sdf
import omni.usd

# Get the current stage
stage = omni.usd.get_context().get_stage()

# Create the ROS2Bridge node
create_prim("/World/ROS2Bridge", "IsaacSimROS2Bridge")

# TF Publisher
create_prim("/World/ROS2Bridge/TFPublisher", "ROS2PublishTransformTree")
tf_prim = stage.GetPrimAtPath("/World/ROS2Bridge/TFPublisher")
tf_prim.CreateAttribute("topicName", Sdf.ValueTypeNames.Token).Set("/tf")
tf_prim.CreateAttribute("targetPrims", Sdf.ValueTypeNames.TokenArray).Set(["/World/ur3e/base_link"])
tf_prim.CreateAttribute("useSimulationTime", Sdf.ValueTypeNames.Bool).Set(True)

# Joint State Publisher
create_prim("/World/ROS2Bridge/JointStatePublisher", "ROS2PublishJointState")
js_prim = stage.GetPrimAtPath("/World/ROS2Bridge/JointStatePublisher")
js_prim.CreateAttribute("topicName", Sdf.ValueTypeNames.Token).Set("/joint_states")
js_prim.CreateAttribute("targetPrim", Sdf.ValueTypeNames.Token).Set("/World/ur3e")
js_prim.CreateAttribute("useSimulationTime", Sdf.ValueTypeNames.Bool).Set(True)
