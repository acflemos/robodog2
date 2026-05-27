# rbd_slam_x3_launch.py
# ======================
# SLAM em simulação Gazebo — gera o mapa ~/rbd_mapa_moveis.yaml da casa.
#
# Etapa única de mapeamento: percorrer a casa com teleop enquanto o
# slam_toolbox constrói o mapa em tempo real. Guardar quando pronto.
#
# O que lança:
#   1. rbd_casa_x3_launch.py — Gazebo + X3 em cma_moveis.world (-3.0, -2.0)
#   2. slam_toolbox (async_slam_toolbox_node) — SLAM 2D online
#   3. RViz2 com map.rviz — visualiza /map + /scan + TF em tempo real
#
# Fluxo completo para gerar ~/rbd_mapa_moveis.yaml:
#   Terminal 1: rbd2_slam_x3            (este launch — Gazebo + SLAM + RViz)
#   Terminal 2: rbd2_teclado            (percorrer a casa)
#   Terminal 2: rbd2_salva_mapa_moveis  (quando o mapa estiver completo)
#   Depois:     rbd2_simulador_x3       (simulador completo com o mapa)
#
# Uso:
#   ros2 launch robodog2 rbd_slam_x3_launch.py
#
# Alias:
#   alias rbd2_slam_x3='ros2 launch robodog2 rbd_slam_x3_launch.py'

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')
    pkg_nav = get_package_share_directory('yahboomcar_nav')

    slam_params = os.path.join(pkg_nav, 'params', 'rbd_slam_toolbox_params.yaml')
    rviz_config = os.path.join(pkg_nav, 'rviz', 'map.rviz')

    # Passo 1: Gazebo + X3 em cma_moveis.world, spawn em (-3.0, -2.0)
    casa_x3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'rbd_casa_x3_launch.py')
        ),
        launch_arguments={'rviz': 'false'}.items()
    )

    # Passo 2: slam_toolbox — mapeamento 2D online assíncrono
    #   Publica: /map (OccupancyGrid), TF map→odom
    #   Subscreve: /scan, TF odom→base_footprint (via Gazebo planar_move plugin)
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
        casa_x3,
        slam_node,
        rviz_node,
    ])
