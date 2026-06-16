# rbd_slam_x3_launch.py
# ======================
# SLAM em simulação Gazebo Fortress — gera mapa da casa (vazia ou com móveis).
#
# Etapa única de mapeamento: percorrer a casa com teleop enquanto o
# slam_toolbox constrói o mapa em tempo real. Guardar quando pronto.
#
# O que lança:
#   1. rbd_gz_x3_launch.py — Gazebo Fortress + X3 no mundo escolhido
#   2. slam_toolbox (async_slam_toolbox_node) — SLAM 2D online
#   3. RViz2 com map.rviz — visualiza /map + /scan + TF em tempo real
#
# Fluxo completo:
#   Terminal 1: rbd2_slam_x3_vazio        — Gazebo + SLAM + RViz (casa vazia)
#            ou rbd2_slam_x3_moveis       — Gazebo + SLAM + RViz (casa com móveis)
#   Terminal 2: rbd2_teclado              — percorrer a casa
#   Terminal 2: rbd2_salva_mapa_vazio     — salvar ~/rbd_mapa_vazio.yaml
#            ou rbd2_salva_mapa_moveis    — salvar ~/rbd_mapa_moveis.yaml
#   Depois:     rbd2_simulador_x3        — simulador completo com o mapa
#
# Uso:
#   ros2 launch robodog2 rbd_slam_x3_launch.py                          (casa vazia — default)
#   ros2 launch robodog2 rbd_slam_x3_launch.py world:=cma_moveis.world  (casa com móveis)
#
# Aliases:
#   alias rbd2_slam_x3_vazio='ros2 launch robodog2 rbd_slam_x3_launch.py'
#   alias rbd2_slam_x3_moveis='ros2 launch robodog2 rbd_slam_x3_launch.py world:=cma_moveis.world'

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')

    slam_params = os.path.join(pkg_robodog2, 'params', 'rbd_slam_toolbox_params.yaml')
    rviz_config = os.path.join(pkg_robodog2, 'rviz', 'map.rviz')

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value='cma_vazio.world',
        description='Mundo Gazebo: cma_vazio.world (default) ou cma_moveis.world'
    )

    # Passo 1: Gazebo Fortress + X3 no mundo escolhido, spawn em (-3.0, -2.0)
    casa_x3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'rbd_gz_x3_launch.py')
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'rviz': 'false',
        }.items()
    )

    # Passo 2: slam_toolbox — mapeamento 2D online assíncrono
    #   Publica: /map (OccupancyGrid), TF map→odom
    #   Subscreve: /scan, TF odom→base_footprint (via Gazebo odometry publisher)
    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_params, {'use_sim_time': True}],
    )

    # Passo 3: RViz2 — visualiza mapa em construção + scan + TF
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        casa_x3,
        slam_node,
        rviz_node,
    ])
