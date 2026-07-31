# rbd_bringup.launch.py
# ======================
# Nav2 + RViz2 para o ROSMASTER X3 em hardware real (sem Gazebo).
#
# Pré-requisito: rbd_robo_hardware_launch.py já a correr no robô
#   (drivers Yahboom + RPLIDAR A1 publicam /scan, /odom e TF)
#
# O que lança:
#   1. navigation_dwa_launch.py — Nav2 (AMCL + DWB + BT Navigator + recoveries)
#      com use_sim_time=false e parâmetros do ficheiro rbd_dwa_nav_params_real.yaml
#   2. RViz2 — visualização (opcional, default: false — o robô não tem ecrã)
#   3. rbd_navega — patrulha autónoma por pesos (opcional, default: false)
#
# Uso (no PC ou no robô, com rede ROS2 configurada):
#   ros2 launch robodog2 rbd_bringup.launch.py map:=<caminho_para_mapa.yaml>
#   ros2 launch robodog2 rbd_bringup.launch.py map:=<mapa.yaml> rviz:=true
#   ros2 launch robodog2 rbd_bringup.launch.py map:=<mapa.yaml> navega:=true
#
# Aliases (no PC ou no robô):
#   alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py map:=$(ros2 pkg prefix robodog2)/share/robodog2/maps/rbd_mapa_vazio.yaml'
#   alias rbd2_bringup_rviz='ros2 launch robodog2 rbd_bringup.launch.py rviz:=true map:=$(ros2 pkg prefix robodog2)/share/robodog2/maps/rbd_mapa_vazio.yaml'
#
# Fluxo completo no robô real:
#   Terminal 1 (robô): rbd2_robo_hardware   ← drivers + lidar
#   Terminal 2 (PC):   rbd2_bringup         ← Nav2 + RViz
#   Terminal 3 (PC):   rbd2_navega          ← patrulha autónoma
#
# Nota sobre a pose inicial:
#   Ao contrário da simulação, aqui set_initial_pose=false.
#   Após lançar, usar o botão "2D Pose Estimate" no RViz2 para definir
#   onde o robô está no mapa antes de iniciar a navegação.

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
    default_map = os.path.join(pkg_robodog2, 'maps', 'rbd_mapa_vazio.yaml')
    real_params = os.path.join(pkg_robodog2, 'params', 'rbd_dwa_nav_params_real.yaml')
    rviz_config = os.path.join(pkg_robodog2, 'rviz', 'robodog2.rviz')

    map_arg = DeclareLaunchArgument(
        name='map',
        default_value=default_map,
        description='Caminho para o YAML do mapa gravado com SLAM'
    )

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Lançar RViz2 (true/false). Default false: robô não tem ecrã'
    )

    navega_arg = DeclareLaunchArgument(
        name='navega',
        default_value='false',
        choices=['true', 'false'],
        description='Lançar rbd_navega (patrulha autónoma). Default false: iniciar manualmente'
    )

    # Nav2: AMCL (localização no mapa) + DWB (planeamento local) + BT Navigator
    # use_composition=False: no robô real (Pi 4B), a composição padrão do
    # nav2_bringup pode sofrer timeout ao carregar o AMCL sob carga — ver
    # comentário em navigation_dwa_launch.py.
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'navigation_dwa_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'false',
            'map': LaunchConfiguration('map'),
            'params_file': real_params,
            'use_composition': 'False',
        }.items()
    )

    # RViz2 — útil quando a correr no PC remoto via rede ROS2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': False}],
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # rbd_navega — loop autónomo de patrulha por pesos
    navega_node = Node(
        package='robodog2',
        executable='rbd_navega',
        name='rbd_navega',
        output='screen',
        condition=IfCondition(LaunchConfiguration('navega'))
    )

    return LaunchDescription([
        map_arg,
        rviz_arg,
        navega_arg,
        nav2,
        rviz_node,
        navega_node,
    ])
