from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robodog2',
            executable='rbd_navega',
            name='rbd_navega',
            output='screen',
        ),
    ])
