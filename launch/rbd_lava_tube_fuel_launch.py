# rbd_lava_tube_fuel_launch.py — Lava tube Fuel puro (DARPA SubT).
#
# Uso (alias validado):
#   rbd_lava_tube_fuel
#
# Spawn sobre walking_plate, fora da boca do túnel (topo da placa em z=3.5 m).
# Pré-requisito: rbd2_build_pkg && rbd2_source (instala lava_tube_fuel.world)

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
                'world': 'lava_tube_fuel.world',
                'spawn_x': '-5.0',
                'spawn_y': '0.0',
                'spawn_z': '3.51',
            }.items(),
        ),
    ])