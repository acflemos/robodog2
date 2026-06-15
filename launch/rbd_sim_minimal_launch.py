# rbd_sim_minimal_launch.py
# ==========================
# Launch mínimo de simulação — diagnóstico e referência.
#
# Objetivo: verificar que o robot aparece no Gazebo sem dependências opcionais.
# Se funcionar aqui, a mesma lógica pode ser aplicada ao rbd_casa_x3_launch.py.
#
# O que lança:
#   1. Gazebo com empty.world  — carrega em <5 segundos
#   2. robot_state_publisher   — publica /robot_description e TF
#   3. spawn_entity            — insere o X3 na origem (0, 0, 0)
#
# O que NÃO lança (intencionalmente):
#   - imu_filter_madgwick  — requer dados do sensor IMU do Gazebo
#   - Nav2 / AMCL          — não é necessário para verificar o robot
#   - RViz                 — opcional; usa rviz:=true se quiseres
#
# Uso:
#   ros2 launch robodog2 rbd_sim_minimal_launch.py
#   ros2 launch robodog2 rbd_sim_minimal_launch.py rviz:=true

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')
    urdf_path = os.path.join(pkg_robodog2, 'urdf', 'rbd_X3_sim.urdf.xacro')

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2'
    )

    world_path = PathJoinSubstitution([
        FindPackageShare('robodog2'), 'worlds', 'empty.world'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    # 1. Gazebo pausado com mundo vazio — carrega em segundos
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch'),
            '/gazebo.launch.py'
        ]),
        launch_arguments={
            'world': world_path,
            'pause': 'true',
        }.items()
    )

    # 2. robot_state_publisher — publica /robot_description (necessário para spawn)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # 3. Spawn do X3 na origem
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'rosmaster_x3',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0',
            '-Y', '0.0',
        ],
        output='screen'
    )

    # 4. Retoma física após spawn concluir
    unpause_gazebo = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_entity_node,
            on_exit=[
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call',
                         '/unpause_physics', 'std_srvs/srv/Empty'],
                    output='screen'
                )
            ]
        )
    )

    # 5. RViz2 (opcional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(
            pkg_robodog2, 'rviz', 'nav.rviz'
        )],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        rviz_arg,
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
        unpause_gazebo,
        rviz_node,
    ])
