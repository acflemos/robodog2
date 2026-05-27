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
        # yahboomcar_bringup
        ('share/' + package_name + '/yahboomcar_bringup/launch',
            glob.glob('yahboomcar_bringup/launch/*.py')),
        ('share/' + package_name + '/yahboomcar_bringup/param',
            glob.glob('yahboomcar_bringup/param/*.yaml')),
        ('share/' + package_name + '/yahboomcar_bringup/rviz',
            glob.glob('yahboomcar_bringup/rviz/*.rviz')),
        # yahboomcar_description — meshes (subpastas)
        ('share/' + package_name + '/yahboomcar_description/urdf',
            glob.glob('yahboomcar_description/urdf/*.xacro') +
            glob.glob('yahboomcar_description/urdf/*.urdf')),
        ('share/' + package_name + '/yahboomcar_description/launch',
            glob.glob('yahboomcar_description/launch/*.py')),
        ('share/' + package_name + '/yahboomcar_description/rviz',
            glob.glob('yahboomcar_description/rviz/*.rviz')),
        ('share/' + package_name + '/yahboomcar_description/meshes',
            glob.glob('yahboomcar_description/meshes/*.STL')),
        ('share/' + package_name + '/yahboomcar_description/meshes/mecanum',
            glob.glob('yahboomcar_description/meshes/mecanum/*.STL')),
        ('share/' + package_name + '/yahboomcar_description/meshes/Ackermann',
            glob.glob('yahboomcar_description/meshes/Ackermann/*.STL')),
        ('share/' + package_name + '/yahboomcar_description/meshes/sensor',
            glob.glob('yahboomcar_description/meshes/sensor/*.STL')),
        # yahboomcar_nav
        ('share/' + package_name + '/yahboomcar_nav/launch',
            glob.glob('yahboomcar_nav/launch/*.py')),
        ('share/' + package_name + '/yahboomcar_nav/params',
            glob.glob('yahboomcar_nav/params/*.yaml') +
            glob.glob('yahboomcar_nav/params/*.lua')),
        ('share/' + package_name + '/yahboomcar_nav/rviz',
            glob.glob('yahboomcar_nav/rviz/*.rviz')),
        ('share/' + package_name + '/yahboomcar_nav/maps',
            glob.glob('yahboomcar_nav/maps/*.pgm') +
            glob.glob('yahboomcar_nav/maps/*.yaml')),
        # yahboomcar_laser
        ('share/' + package_name + '/yahboomcar_laser/launch',
            glob.glob('yahboomcar_laser/launch/*.py')),
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
        ],
    },
)
