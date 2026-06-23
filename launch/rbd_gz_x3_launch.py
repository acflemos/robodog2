# rbd_gz_x3_launch.py
# ====================
# Gazebo Fortress (Ignition Gazebo v6) + ROSMASTER X3 + ROS2 Humble.
#
# Lança o simulador Gazebo com o robô spawnado em (-3.0, -2.0).
# Usado como base por rbd_simulador_x3_launch.py e rbd_slam_x3_launch.py.
#
# Uso direto (Gazebo isolado, sem Nav2):
#   ros2 launch robodog2 rbd_gz_x3_launch.py
#   ros2 launch robodog2 rbd_gz_x3_launch.py rviz:=true
#   ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world
#   rbd_lava_tube       — alias para lava_tube.world (v1 aprovada, spawn na entrada)
#   rbd_lava_tube_fuel  — alias para lava_tube_fuel.world (meshes Fuel DARPA SubT)

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

    # Permite que o Ignition Gazebo encontre os arquivos model://robodog2/meshes/...
    # O share/ contém a pasta robodog2/ que o Gazebo usa como raiz do modelo.
    set_ign_resource_path = AppendEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(pkg_robodog2, '..')
    )

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value='rbd_gz_empty.world',
        description='Arquivo world em share/robodog2/worlds/'
    )

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Abrir RViz2'
    )

    spawn_x_arg = DeclareLaunchArgument(
        name='spawn_x',
        default_value='-3.0',
        description='Posição X do spawn do robô'
    )

    spawn_y_arg = DeclareLaunchArgument(
        name='spawn_y',
        default_value='-2.0',
        description='Posição Y do spawn do robô'
    )

    spawn_z_arg = DeclareLaunchArgument(
        name='spawn_z',
        default_value='0.1',
        description='Posição Z do spawn do robô (lava_tube: 0.01)'
    )

    world_path = [
        os.path.join(pkg_robodog2, 'worlds', ''),
        LaunchConfiguration('world'),
    ]

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    # 1. Servidor Gazebo Fortress
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
            '-x', LaunchConfiguration('spawn_x'),
            '-y', LaunchConfiguration('spawn_y'),
            '-z', LaunchConfiguration('spawn_z'),
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

    # 6. RViz2 (opcional)
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
        spawn_x_arg,
        spawn_y_arg,
        spawn_z_arg,
        gz_server,
        gz_gui,
        robot_state_publisher,
        spawn_robot,
        bridge,
        rviz_node,
    ])
