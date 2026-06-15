# rbd_simulador_x3_launch.py
# ==========================
# Simulador completo: Gazebo Fortress + Nav2 (AMCL omni + DWB) + RViz.
#
# Pré-requisito: mapa da casa gerado com rbd2_slam_x3_vazio ou rbd2_slam_x3_moveis.
#   ~/rbd_mapa_vazio.yaml   (casa vazia — gerado em 2026-06-10)
#   ~/rbd_mapa_moveis.yaml  (casa com móveis — gerar com rbd2_slam_x3_moveis)
#
# O que lança:
#   1. rbd_gz_x3_launch.py  — Gazebo Fortress + X3 no mundo escolhido
#   2. navigation_dwa_launch.py — Nav2 (AMCL + DWB + BT Navigator + recoveries)
#   3. RViz2 com robodog2.rviz — visualiza mapa + costmaps + TF + scan + Nav2 panel
#
# Fluxo completo:
#   Terminal 1: rbd2_simulador_x3          — Gazebo + Nav2 + RViz (mapa vazio — default)
#            ou rbd2_simulador_x3_moveis   — Gazebo + Nav2 + RViz (mapa com móveis)
#   Terminal 2: rbd2_navega               — loop autónomo de patrulha por pesos
#   Terminal 2: rbd2_teclado             — teleop manual alternativo
#
# Uso:
#   ros2 launch robodog2 rbd_simulador_x3_launch.py
#   ros2 launch robodog2 rbd_simulador_x3_launch.py world:=cma_moveis.world map:=$HOME/rbd_mapa_moveis.yaml
#
# Aliases:
#   alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py'
#   alias rbd2_simulador_x3_moveis='ros2 launch robodog2 rbd_simulador_x3_launch.py world:=cma_moveis.world map:=$HOME/rbd_mapa_moveis.yaml'
#
# Hardware real (sem Gazebo):
#   Terminal 1: rbd2_bringup
#   Terminal 2: ros2 launch robodog2 rbd_simulador_x3_launch.py sim:=false map:=<caminho>

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')
    default_map = os.path.join(os.path.expanduser('~'), 'rbd_mapa_vazio.yaml')
    sim_params = os.path.join(pkg_robodog2, 'params', 'rbd_dwa_nav_params.yaml')
    rviz_config = os.path.join(pkg_robodog2, 'rviz', 'robodog2.rviz')

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value='cma_vazio.world',
        description='Mundo Gazebo: cma_vazio.world (default) ou cma_moveis.world'
    )

    map_arg = DeclareLaunchArgument(
        name='map',
        default_value=default_map,
        description='Caminho para o ficheiro YAML do mapa (default: ~/rbd_mapa_vazio.yaml)'
    )

    sim_arg = DeclareLaunchArgument(
        name='sim',
        default_value='true',
        choices=['true', 'false'],
        description='true=simulação (lança Gazebo + use_sim_time), false=hardware real'
    )

    # Passo 1: Gazebo Fortress + X3 no mundo escolhido (apenas em modo simulação)
    casa_x3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'rbd_gz_x3_launch.py')
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'rviz': 'false',
        }.items(),
        condition=IfCondition(LaunchConfiguration('sim'))
    )

    # Passo 2: Nav2 — AMCL (OmniMotionModel) + DWB + BT Navigator + recoveries
    #   Publica: TF map→odom (AMCL), /cmd_vel (DWB)
    #   Subscreve: /scan, /odom, TF odom→base_footprint
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'navigation_dwa_launch.py')
        ),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('sim'),
            'map': LaunchConfiguration('map'),
            'params_file': sim_params,
        }.items()
    )

    # Passo 3: RViz2 — mapa + costmaps + TF + scan + seta de goal
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('sim')}],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        map_arg,
        sim_arg,
        casa_x3,
        nav2,
        rviz_node,
    ])
