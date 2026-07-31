# navigation_dwa_launch.py
# =========================
# Nav2 com planejador local DWB (Dynamic Window-Based).
# Incluído pelo rbd_simulador_x3_launch.py — não usar diretamente.
#
# Argumentos (passados pelo rbd_simulador_x3_launch.py):
#   use_sim_time  — true em simulação, false em hardware real
#   map           — caminho para o .yaml do mapa
#   params_file   — caminho para o YAML de parâmetros Nav2
#
# Pipeline Nav2 (via nav2_bringup):
#   AMCL (OmniMotionModel) → localização probabilística com mapa
#   DWB (controller_server) → planejador local de trajetória
#   NavFn (planner_server)  → planejador global (Dijkstra/A*)
#   BT Navigator            → coordena o pipeline de navegação
#   recoveries_server       → spin, backup, wait em caso de bloqueio
#
# Parâmetros ativos em robodog2: params/rbd_dwa_nav_params.yaml

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_path = get_package_share_directory('robodog2')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_yaml_path = LaunchConfiguration(
        'map', default=os.path.join(package_path, 'maps', 'rbd_mapa_vazio.yaml'))
    nav2_param_path = LaunchConfiguration('params_file', default=os.path.join(
        package_path, 'params', 'rbd_dwa_nav_params.yaml'))
    # use_composition=True (default do nav2_bringup) carrega todos os nós Nav2
    # num único processo via chamadas de serviço ROS2. Na Raspberry Pi 4B, sob
    # carga, essas chamadas podem sofrer timeout — quando isso acontece no
    # carregamento do map_server, o nav2_bringup aborta silenciosamente o
    # resto do grupo de localização e o AMCL nunca sobe (sem erro visível).
    # No robô real usamos processos separados (use_composition=False) para
    # evitar esse timeout; em simulação (PC) o composition continua ligado.
    use_composition = LaunchConfiguration('use_composition', default='True')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value=use_sim_time,
                              description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('map', default_value=map_yaml_path,
                              description='Full path to map file to load'),
        DeclareLaunchArgument('params_file', default_value=nav2_param_path,
                              description='Full path to param file to load'),
        DeclareLaunchArgument('use_composition', default_value=use_composition,
                              description='Nav2 em processo único (composição) — desligar no robô real (Pi 4B)'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir, '/launch', '/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path,
                'use_composition': use_composition}.items(),
        ),
    ])
