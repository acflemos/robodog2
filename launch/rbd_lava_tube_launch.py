# rbd_lava_tube_launch.py — Lava tube v1 aprovada (caixa oca, primitivas).
#
# Uso (alias validado):
#   rbd_lava_tube

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg = get_package_share_directory('robodog2')
    base = os.path.join(pkg, 'launch', 'rbd_gz_x3_launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(base),
            launch_arguments={
                'world': 'lava_tube.world',
                'spawn_x': '-2.0',
                'spawn_y': '0.0',
                'spawn_z': '0.01',
            }.items(),
        ),
    ])