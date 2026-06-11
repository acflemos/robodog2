import glob
from setuptools import find_packages, setup

package_name = 'robodog2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files principais
        ('share/' + package_name + '/launch', glob.glob('launch/*.py')),
        # URDF e xacro
        ('share/' + package_name + '/urdf',
            glob.glob('urdf/*.xacro') + glob.glob('urdf/*.urdf')),
        # Mundos Gazebo
        ('share/' + package_name + '/worlds', glob.glob('worlds/*.world')),
        ('share/' + package_name + '/worlds/gz', glob.glob('worlds/gz/*.world')),
        ('share/' + package_name + '/worlds/robodog1_classic', glob.glob('worlds/robodog1_classic/*.world')),
        # Malhas STL (visual Gazebo/RViz)
        ('share/' + package_name + '/meshes/mecanum', glob.glob('meshes/mecanum/*.STL')),
        ('share/' + package_name + '/meshes/sensor', glob.glob('meshes/sensor/*.STL')),
        # Configuração de bridges ROS↔Gazebo
        ('share/' + package_name + '/config', glob.glob('config/*.yaml')),
        # Parâmetros Nav2 (git-tracked — substituem yahboomcar_nav para simulação)
        ('share/' + package_name + '/params', glob.glob('params/*.yaml')),
        # Configurações RViz (rbd_nav.rviz, rbd_map.rviz — copiados do yahboomcar_nav)
        ('share/' + package_name + '/rviz', glob.glob('rviz/*.rviz')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='antonio',
    maintainer_email='antolemos@gmail.com',
    description='Robodog2 — robô de vigilância doméstica com comportamento autônomo, ROS2 Humble, hardware ROSMaster X3',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rbd_navega = robodog2.rbd_navega:main',
            'rbd_nav_simples = robodog2.rbd_nav_simples:main',
        ],
    },
)
