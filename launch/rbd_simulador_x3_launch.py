# rbd_simulador_x3_launch.py
# ==========================
# Equivalente ROS2 do alias rbd_simulador_x3 do robodog1 (ROS1/Noetic).
#
# Lança o simulador completo em um único comando:
#   Passo 1 — Gazebo com cma_moveis.world + spawn do X3 em (-3.0, -2.0)  [rbd_casa_x3_launch.py]
#   Passo 2 — Nav2: AMCL (omni) + DWB planner + mapa pré-construído      [navigation_dwa_launch.py]
#   Passo 3 — RViz2 com configuração de navegação                         [nav.rviz]
#
# Diferenças em relação ao robodog_simulador_x3.launch (ROS1):
#   - move_base (ROS1) → Nav2 bt_navigator + controller_server + planner_server (ROS2)
#   - map_server (ROS1) → nav2_map_server dentro do nav2_bringup (ROS2)
#   - use_sim_time propagado a todos os nós via rbd_sim_dwa_params.yaml
#   - AMCL pose inicial (-3.0, -2.0) definida em rbd_sim_dwa_params.yaml (não no launch)
#
# Pré-requisito — mapa da casa:
#   O ficheiro ~/rbd_mapa_moveis.yaml deve existir antes de lançar.
#   Para gerar: lançar rbd_casa_x3_launch.py + teleop + guardar:
#     ros2 run nav2_map_server map_saver_cli -f ~/rbd_mapa_moveis
#   Alias: rbd2_salva_mapa_moveis
#
# Argumentos:
#   map  (default: ~/rbd_mapa_moveis.yaml) — mapa pré-construído da casa
#
# Uso:
#   ros2 launch robodog2 rbd_simulador_x3_launch.py
#   ros2 launch robodog2 rbd_simulador_x3_launch.py map:=/caminho/para/mapa.yaml
#
# Alias (equiv. ao antigo rbd_simulador_x3 do robodog1):
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
    pkg_robodog2 = get_package_share_directory('robodog2')
    pkg_nav = get_package_share_directory('yahboomcar_nav')

    default_map = os.path.join(os.path.expanduser('~'), 'rbd_mapa_moveis.yaml')
    sim_params = os.path.join(pkg_nav, 'params', 'rbd_sim_dwa_params.yaml')
    rviz_config = os.path.join(pkg_nav, 'rviz', 'nav.rviz')

    map_arg = DeclareLaunchArgument(
        name='map',
        default_value=default_map,
        description='Caminho para o ficheiro YAML do mapa da casa'
    )

    # Passo 1: Gazebo + X3 em cma_moveis.world, spawn em (-3.0, -2.0)
    casa_x3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robodog2, 'launch', 'rbd_casa_x3_launch.py')
        ),
        launch_arguments={'rviz': 'false'}.items()
    )

    # Passo 2: Nav2 — AMCL (omni) + DWB + mapa
    #   rbd_sim_dwa_params.yaml: use_sim_time=True + pose inicial (-3.0,-2.0)
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav, 'launch', 'navigation_dwa_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'map': LaunchConfiguration('map'),
            'params_file': sim_params,
        }.items()
    )

    # Passo 3: RViz2 com configuração de navegação (mapa + laser + costmaps + TF)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        map_arg,
        casa_x3,
        nav2,
        rviz_node,
    ])
