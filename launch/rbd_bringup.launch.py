# rbd_bringup.launch.py
# ======================
# Bringup do ROSMASTER X3 em hardware real (sem Gazebo).
#
# Lança o nó rbd_navega para operação autônoma no robô físico.
# Pré-requisito: Nav2 e sensores do X3 já ativos via bringup do Yahboom.
#
# Uso:
#   alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py'

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
