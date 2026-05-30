# rbd_casa_x3_launch.py
# ======================
# Equivalente ROS2 do alias rbd_casa_x3 do robodog1 (ROS1/Noetic).
#
# Lança o Gazebo com o mundo 3D da casa (cma_moveis.world) e spawna o X3
# na mesma posição inicial usada no robodog1: (-3.0, -2.0, 0.0).
#
# Responsabilidade (igual ao original ROS1 robodog_casa_x3.launch):
#   - Inicia o Gazebo PAUSADO — física congelada durante o carregamento dos 178 modelos
#   - Carrega rbd_X3_sim.urdf.xacro como robot_description
#   - Insere o ROSMASTER X3 na cena via spawn_entity
#   - Retoma a física logo após o spawn concluir (OnProcessExit → /unpause_physics)
#   - NÃO inicia navegação, AMCL, Nav2 nem RViz (por defeito)
#
# Porquê iniciar pausado:
#   O cma_moveis.world tem 178 modelos que levam ~2 min a carregar.
#   Se a física estiver activa durante esse tempo o robot pode ser deslocado
#   por colisões com paredes que aparecem à sua volta.
#   Iniciando pausado, o robot é colocado com segurança e a física só começa
#   depois do spawn estar concluído.
#
# É o ponto de entrada para qualquer launch que precise de simulação em casa:
#   rbd_nav_sim_launch.py deve incluir este launch + Nav2/SLAM.
#
# Uso:
#   ros2 launch robodog2 rbd_casa_x3_launch.py
#   ros2 launch robodog2 rbd_casa_x3_launch.py rviz:=true
#
# Alias (equiv. ao antigo rbd_casa_x3 do robodog1):
#   alias rbd2_casa_x3='ros2 launch robodog2 rbd_casa_x3_launch.py'
#
# Referência ROS1:
#   robodog1/launch/rbd/robodog_casa_x3.launch

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
    imu_filter_config = os.path.join(
        get_package_share_directory('yahboomcar_bringup'), 'param', 'imu_filter_param.yaml'
    )
    default_rviz_config = os.path.join(
        get_package_share_directory('yahboomcar_nav'), 'rviz', 'nav.rviz'
    )

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2 com configuração de navegação'
    )

    # Mundo 3D da casa com móveis — caminho absoluto no install do robodog2
    world_path = PathJoinSubstitution([
        FindPackageShare('robodog2'), 'worlds', 'cma_moveis.world'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    # 1. Gazebo PAUSADO — equiv. a paused:=true do robodog1 empty_world.launch
    #    A física só arranca depois do spawn (evita deslocamento durante o carregamento)
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

    # 2. Publica robot_description e TF dos joints
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # 3. Insere o X3 na cena Gazebo na posição inicial da casa
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'rosmaster_x3',
            '-x', '-3.0',
            '-y', '-2.0',
            '-z', '0.0',
            '-Y', '0.0',
        ],
        output='screen'
    )

    # 4. Retoma a física logo após o spawn concluir
    #    OnProcessExit dispara quando spawn_entity.py termina com sucesso
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

    # 5. Filtro IMU: /imu/data_raw (Gazebo) → /imu/data (orientação fundida)
    imu_filter_node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        parameters=[imu_filter_config, {'use_sim_time': True}]
    )

    # 6. RViz2 (opcional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', default_rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        rviz_arg,
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
        unpause_gazebo,
        imu_filter_node,
        rviz_node,
    ])
