# rbd_simulador_x3_launch.py
# ==========================
# Lança Nav2 (AMCL + DWB) + RViz2 sobre uma fonte de sensores já activa.
#
# NÃO lança o Gazebo. Deve ser chamado depois de rbd2_casa_x3 (simulação)
# ou depois do bringup do hardware real (rosmaster X3).
#
# Fluxo simulação:
#   Terminal 1: rbd2_casa_x3        ← Gazebo + robô em cma_moveis.world
#   Terminal 2: rbd2_simulador_x3   ← Nav2 + RViz2 (este ficheiro)
#
# Fluxo hardware real (X3 físico na posição equivalente ao spawn):
#   Terminal 1: rbd2_bringup        ← bringup do hardware
#   Terminal 2: rbd2_simulador_x3 sim:=false  ← Nav2 + RViz2
#
# Pré-requisito — mapa da casa:
#   ~/rbd_mapa_moveis.yaml deve existir.
#   Para gerar com simulação: rbd2_slam_x3 + rbd2_teclado + rbd2_salva_mapa_moveis
#
# Argumentos:
#   map      (default: ~/rbd_mapa_moveis.yaml)
#   sim      (default: true) — true=use_sim_time, false=hardware real
#
# Alias:
#   alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py'
#
# Referência ROS1:
#   robodog1/launch/rbd/robodog_simulador_x3.launch

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    default_map = os.path.join(os.path.expanduser('~'), 'rbd_mapa_moveis.yaml')
    sim_params = os.path.join(get_package_share_directory('yahboomcar_nav'), 'params', 'rbd_sim_dwa_params.yaml')
    rviz_config = os.path.join(get_package_share_directory('robodog2'), 'rviz', 'robodog2.rviz')

    map_arg = DeclareLaunchArgument(
        name='map',
        default_value=default_map,
        description='Caminho para o ficheiro YAML do mapa da casa'
    )

    sim_arg = DeclareLaunchArgument(
        name='sim',
        default_value='true',
        choices=['true', 'false'],
        description='true=simulação (use_sim_time), false=hardware real'
    )

    # Nav2 — AMCL (omni) + DWB + mapa pré-construído
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('yahboomcar_nav'), 'launch', 'navigation_dwa_launch.py')
        ),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('sim'),
            'map': LaunchConfiguration('map'),
            'params_file': sim_params,
        }.items()
    )

    # RViz2 com configuração de navegação (mapa + laser + costmaps + TF)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('sim')}],
        output='screen'
    )

    return LaunchDescription([
        map_arg,
        sim_arg,
        nav2,
        rviz_node,
    ])
