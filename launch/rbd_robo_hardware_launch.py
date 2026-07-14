# rbd_robo_hardware_launch.py
# ============================
# Camada de hardware do ROSMASTER X3 — corre APENAS no robô físico.
#
# O que lança:
#   1. yahboomcar_bringup_X3_launch.py — driver do Arduino (Mcnamu_driver_X3),
#      cinemática mecanum (base_node_X3), fusão IMU (Madgwick + EKF),
#      robot_state_publisher com o URDF real do X3
#   2. sllidar_launch.py (sllidar_ros2) — driver do RPLIDAR A1,
#      publica /scan em LaserScan
#
# Pré-requisito no robô:
#   - pacote sllidar_ros2 instalado (sudo apt install ros-humble-sllidar-ros2)
#   - RPLIDAR A1 ligado em /dev/ttyUSB0 (verificar com: ls /dev/ttyUSB*)
#   - Arduino do X3 ligado e acessível (Rosmaster_Lib)
#
# Uso (no robô, dentro do container ROS2):
#   ros2 launch robodog2 rbd_robo_hardware_launch.py
#
# Alias (no robô):
#   alias rbd2_robo_hardware='ros2 launch robodog2 rbd_robo_hardware_launch.py'
#
# Fluxo completo no robô real:
#   Terminal 1 (robô): rbd2_robo_hardware    ← este launch
#   Terminal 2 (PC):   rbd2_bringup          ← Nav2 + RViz (pode correr no PC via rede ROS2)
#   Terminal 3 (PC):   rbd2_navega           ← patrulha autónoma

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Driver de hardware X3: motor, IMU, odometria, EKF, robot_state_publisher
    yahboom_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('yahboomcar_bringup'),
                'launch',
                'yahboomcar_bringup_X3_launch.py'
            )
        )
    )

    # Driver do RPLIDAR A1 — publica /scan
    # Pacote: sllidar_ros2 (instalar com: sudo apt install ros-humble-sllidar-ros2)
    # Por defeito: porta /dev/ttyUSB0, baudrate 115200
    rplidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('sllidar_ros2'),
                'launch',
                'sllidar_launch.py'
            )
        )
    )

    return LaunchDescription([
        yahboom_bringup,
        rplidar,
    ])
