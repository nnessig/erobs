import rclpy
from sensor_msgs.msg import JointState

from omni.isaac.core import SimulationContext
from omni.isaac.core.utils.extensions import enable_extension, is_extension_enabled
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.articulations import Articulation

# 1 make sure the ROS2 bridge is loaded
if not is_extension_enabled("isaacsim.ros2.bridge"):
    enable_extension("isaacsim.ros2.bridge")

# 2 init ROS2 (idempotent)
try:
    rclpy.init()
except RuntimeError:
    pass

# 3 create the sim (keep your GUI–since you’re already forwarding DISPLAY)
sim = SimulationContext(
    physics_dt=1.0/60.0,
    rendering_dt=1.0/60.0,
    headless=False,
)

# 4 load your UR3e USD (adjust path if needed)
robot_prim = "/World/ur3e"
usd_path   = "/workspace/isaac-sim/isaac-assets/Assets/Isaac/4.5/Isaac/Robots/UniversalRobots/ur3e/ur3e.usd"
add_reference_to_stage(usd_path=usd_path, prim_path=robot_prim)

# 5 set up ROS2 node & publisher
node = rclpy.create_node("ur3e_state_publisher")
pub  = node.create_publisher(JointState, "/joint_states", 10)

# 6 wrap the articulation
art = Articulation(prim_path=robot_prim)

# 7 callback to run each physics tick
def publish_joint_states(dt: float):
    js = JointState()
    js.header.stamp = node.get_clock().now().to_msg()
    js.name     = art.joint_names
    js.position = art.get_joint_positions().tolist()
    pub.publish(js)

sim.add_physics_callback(publish_joint_states)

# 8 start simulation
sim.play()

# 9 clean up on exit
rclpy.shutdown()
print("UR3e spawned and /joint_states is live.")
