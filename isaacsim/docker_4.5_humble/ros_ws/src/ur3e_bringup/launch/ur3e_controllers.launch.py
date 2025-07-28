from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                '/workspace/erobs/isaacsim/config/ur3e_isaac_ros2_control.yaml',
                {'robot_description': open('/workspace/erobs/ur3e.urdf').read()}
            ],
            output='screen'
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_trajectory_controller'],
        ),
    ])

