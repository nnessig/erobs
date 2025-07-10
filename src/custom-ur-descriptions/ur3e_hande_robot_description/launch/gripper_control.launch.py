from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    robot_description_content = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("ur3e_hande_robot_description"),
            "urdf",
            "ur_with_camera_hande.xacro"
        ])
    ])

    return LaunchDescription([
        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[
                {"robot_description": robot_description_content},
                PathJoinSubstitution([
                    FindPackageShare("ur3e_hande_robot_description"),
                    "config",
                    "gripper_controllers.yaml"
                ])
            ],
            output="screen"
        ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["gripper_controller"],
            output="screen"
        )
    ])
