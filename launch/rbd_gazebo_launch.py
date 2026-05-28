# rbd_gazebo_launch.py
# =====================
# Launch principal de simulação Gazebo do robodog2 — ROSMASTER X3 (ROS2 Humble).
#
# O que lança:
#   1. Gazebo Classic — motor de simulação com o world selecionado
#   2. robot_state_publisher — TF de joints a partir de rbd_X3_sim.urdf.xacro
#   3. spawn_entity — injeta o modelo URDF na cena Gazebo
#   4. imu_filter_madgwick — /imu/data_raw (Gazebo IMU) → /imu/data (orientação fundida)
#
# NÃO lança (substituídos pelo Gazebo):
#   - Mcnamu_driver_X3  — driver de hardware (desnecessário em simulação)
#   - base_node_X3      — cinemática (substituído pelo plugin planar_move)
#   - robot_localization EKF — o plugin planar_move já publica /odom limpo
#
# Argumentos:
#   world  (default: empty.world) — ficheiro de mundo Gazebo (relativo a worlds/)
#   rviz   (default: false)       — se 'true', abre RViz2 com a config de navegação
#   x_pos  (default: 0.0)         — posição X inicial do robô (metros)
#   y_pos  (default: 0.0)         — posição Y inicial do robô (metros)
#   z_pos  (default: 0.0)         — posição Z inicial do robô (metros)
#   yaw    (default: 0.0)         — orientação inicial em torno do eixo Z (radianos)
#
# Uso:
#   ros2 launch robodog2 rbd_gazebo_launch.py
#   ros2 launch robodog2 rbd_gazebo_launch.py world:=turtlebot3_world.world
#   ros2 launch robodog2 rbd_gazebo_launch.py world:=cma_moveis.world x_pos:=-3.0 y_pos:=-2.0 rviz:=true
#
# Pré-requisito: colcon build + source install/setup.bash
#
# Subscreve (via Gazebo plugins no URDF):
#   /cmd_vel (Twist) — controlo do robô
# Publica:
#   /scan    (LaserScan) — LiDAR 360°
#   /odom    (Odometry)  — odometria do plugin planar_move
#   /imu/data_raw (Imu) — IMU bruta do Gazebo
#   /imu/data     (Imu) — IMU fundida pelo Madgwick

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')

    urdf_path = os.path.join(pkg_robodog2, 'urdf', 'rbd_X3_sim.urdf.xacro')
    imu_filter_config = os.path.join(get_package_share_directory('yahboomcar_bringup'), 'param', 'imu_filter_param.yaml')
    default_rviz_config = os.path.join(get_package_share_directory('yahboomcar_nav'), 'rviz', 'nav.rviz')

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value='empty.world',
        description='Nome do ficheiro world em robodog2/worlds/ (ex: turtlebot3_world.world)'
    )
    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2 com configuração de navegação'
    )
    x_pos_arg = DeclareLaunchArgument(
        name='x_pos', default_value='0.0',
        description='Posição X inicial do robô (metros)'
    )
    y_pos_arg = DeclareLaunchArgument(
        name='y_pos', default_value='0.0',
        description='Posição Y inicial do robô (metros)'
    )
    z_pos_arg = DeclareLaunchArgument(
        name='z_pos', default_value='0.0',
        description='Posição Z inicial do robô (metros)'
    )
    yaw_arg = DeclareLaunchArgument(
        name='yaw', default_value='0.0',
        description='Orientação inicial em torno do eixo Z (radianos)'
    )

    world_path = PathJoinSubstitution([
        FindPackageShare('robodog2'), 'worlds', LaunchConfiguration('world')
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch'),
            '/gazebo.launch.py'
        ]),
        launch_arguments={'world': world_path}.items()
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'rosmaster_x3',
            '-x', LaunchConfiguration('x_pos'),
            '-y', LaunchConfiguration('y_pos'),
            '-z', LaunchConfiguration('z_pos'),
            '-Y', LaunchConfiguration('yaw'),
        ],
        output='screen'
    )

    imu_filter_node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        parameters=[imu_filter_config, {'use_sim_time': True}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', default_rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        world_arg,
        rviz_arg,
        x_pos_arg,
        y_pos_arg,
        z_pos_arg,
        yaw_arg,
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
        imu_filter_node,
        rviz_node,
    ])
