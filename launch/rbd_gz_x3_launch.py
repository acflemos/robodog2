# rbd_gz_x3_launch.py
# ====================
# Launch para Gazebo Harmonic (Ignition Gazebo 6) + ROS2 Humble.
#
# Substitui rbd_casa_x3_launch.py (Gazebo Classic) após migração.
# Para uso inicial usa o mundo vazio (rbd_gz_empty.world).
# Quando estiver validado, trocar para o mundo da casa.
#
# Uso:
#   ros2 launch robodog2 rbd_gz_x3_launch.py
#   ros2 launch robodog2 rbd_gz_x3_launch.py rviz:=true
#   ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_robodog2 = get_package_share_directory('robodog2')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_path = os.path.join(pkg_robodog2, 'urdf', 'rbd_X3_sim.urdf.xacro')
    bridge_config = os.path.join(pkg_robodog2, 'config', 'rbd_x3_bridge.yaml')

    # Permite que o Ignition Gazebo encontre os ficheiros model://robodog2/meshes/...
    # O share/ contém a pasta robodog2/ que o Gazebo usa como raiz do modelo
    set_ign_resource_path = AppendEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(pkg_robodog2, '..')
    )

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value='rbd_gz_empty.world',
        description='Ficheiro world em share/robodog2/worlds/'
    )

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2'
    )

    world_path = [
        os.path.join(pkg_robodog2, 'worlds', ''),
        LaunchConfiguration('world'),
    ]

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    # 1. Servidor Gazebo Harmonic
    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r -s -v4 '] + world_path,
            'on_exit_shutdown': 'true',
        }.items()
    )

    # 2. GUI Gazebo
    gz_gui = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v4'}.items()
    )

    # 3. Publica robot_description e TF dos joints
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # 4. Insere o robô no mundo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'rosmaster_x3',
            '-topic', 'robot_description',
            '-x', '-3.0',
            '-y', '-2.0',
            '-z', '0.1',
        ],
        output='screen'
    )

    # 5. Bridge ROS ↔ Gazebo (tópicos definidos em rbd_x3_bridge.yaml)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p', f'config_file:={bridge_config}',
        ],
        output='screen'
    )

    # 6. Filtro IMU: /imu/data_raw (bridge) → /imu/data (orientação fundida)
    imu_filter = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        parameters=[{
            'use_sim_time': True,
            'use_mag': False,
            'publish_tf': False,
        }]
    )

    # 7. RViz2 (opcional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        set_ign_resource_path,
        world_arg,
        rviz_arg,
        gz_server,
        gz_gui,
        robot_state_publisher,
        spawn_robot,
        bridge,
        imu_filter,
        rviz_node,
    ])
