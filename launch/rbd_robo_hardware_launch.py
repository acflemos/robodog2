# rbd_robo_hardware_launch.py
# ============================
# Camada de hardware do ROSMASTER X3 — corre APENAS no robô físico.
#
# O que lança:
#   1. yahboomcar_bringup_X3_launch.py — driver do Arduino (Mcnamu_driver_X3),
#      cinemática mecanum (base_node_X3), fusão IMU (Madgwick + EKF),
#      robot_state_publisher com o URDF real do X3
#   2. sllidar_a1_launch.py (sllidar_ros2) — driver do RPLIDAR A1,
#      publica /scan em LaserScan
#
# Pré-requisito no robô:
#   - pacote sllidar_ros2 compilado a partir do source (sem build oficial para
#     arm64 no repo apt do ROS): clonar github.com/Slamtec/sllidar_ros2 no
#     workspace e rodar colcon build --packages-select sllidar_ros2
#   - RPLIDAR A1 ligado em /dev/rplidar (symlink udev fixo — verificar com:
#     ls -la /dev/rplidar). Não depender de /dev/ttyUSBx puro: a numeração
#     pode mudar entre boots conforme a ordem de enumeração USB.
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
    # Pacote: sllidar_ros2 — não tem build oficial para arm64 no repo apt do ROS,
    # precisa ser compilado a partir do source (github.com/Slamtec/sllidar_ros2)
    # dentro do workspace do robô.
    # O launch file é por modelo (sllidar_a1_launch.py para o RPLIDAR A1) — a versão
    # atual do pacote não tem mais um "sllidar_launch.py" genérico.
    # serial_port sobrescrito para "/dev/rplidar" — symlink udev fixo criado no host
    # (idVendor=10c4 idProduct=ea60, chip CP210x), em vez do default "/dev/ttyUSB0"
    # cuja numeração pode mudar entre boots conforme a ordem de enumeração USB.
    # frame_id sobrescrito para "laser_link" — o default do sllidar_ros2 é "laser",
    # mas o URDF real (yahboomcar_description/urdf/yahboomcar_X3.urdf) usa "laser_link".
    # Sem isso, o TF do LiDAR não bate com o resto da árvore.
    rplidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('sllidar_ros2'),
                'launch',
                'sllidar_a1_launch.py'
            )
        ),
        launch_arguments={
            'serial_port': '/dev/rplidar',
            'frame_id': 'laser_link',
        }.items()
    )

    return LaunchDescription([
        yahboom_bringup,
        rplidar,
    ])
