from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time", default_value="true",
            description="Use simulation (Isaac Sim) clock"
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[
                {"use_sim_time": LaunchConfiguration("use_sim_time")},
                {
                    "robot_description": open(
                        "/workspace/ros_ws/install/ur3e.urdf"
                    ).read()
                }
            ],
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=[
                "-d", "/home/developer/ros_ws/rviz/isaacsim-viz.rviz"
            ],
            parameters=[
                {"use_sim_time": LaunchConfiguration("use_sim_time")}
            ],
        )
    ])
