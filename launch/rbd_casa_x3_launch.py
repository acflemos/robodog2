# rbd_casa_x3_launch.py
# ======================
# Equivalente ROS2 do alias rbd_casa_x3 do robodog1 (ROS1/Noetic).
#
# Lança o Gazebo com o mundo 3D da casa (cma_moveis.world) e spawna o X3
# na mesma posição inicial usada no robodog1: (-3.0, -2.0, 0.0).
#
# Responsabilidade (igual ao original ROS1):
#   - Inicia o Gazebo com o mundo 3D da casa
#   - Insere o ROSMASTER X3 na cena
#   - NÃO inicia navegação, AMCL, Nav2 nem RViz (por defeito)
#
# É o ponto de entrada para qualquer launch que precise de simulação em casa:
#   rbd_nav_sim_launch.py deve incluir este launch + Nav2/SLAM.
#
# Uso:
#   ros2 launch robodog2 rbd_casa_x3_launch.py
#   ros2 launch robodog2 rbd_casa_x3_launch.py rviz:=true
#
# Alias (equiv. ao antigo rbd_casa_x3 do robodog1):
#   alias rbd2_casa_x3='ros2 launch robodog2 rbd_casa_x3_launch.py'
#
# Referência ROS1:
#   robodog1/launch/rbd/robodog_casa_x3.launch

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2 com configuração de navegação'
    )

    # Inclui rbd_gazebo_launch.py com os parâmetros fixos da casa:
    #   world:  cma_moveis.world (mundo 3D da casa com móveis)
    #   posição: (-3.0, -2.0, 0.0) — mesma posição do robodog1 robodog_casa_x3.launch
    casa_x3_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'rbd_gazebo_launch.py')
        ),
        launch_arguments={
            'world': 'cma_moveis.world',
            'x_pos': '-3.0',
            'y_pos': '-2.0',
            'z_pos': '0.0',
            'yaw':   '0.0',
            'rviz':  LaunchConfiguration('rviz'),
        }.items()
    )

    return LaunchDescription([
        rviz_arg,
        casa_x3_sim,
    ])
