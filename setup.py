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
        ('share/' + package_name + '/launch', [
            'launch/rbd_bringup.launch.py',
            'launch/rbd_gazebo_launch.py',
        ]),
        ('share/' + package_name + '/urdf', glob.glob('urdf/*.xacro') + glob.glob('urdf/*.urdf')),
        ('share/' + package_name + '/worlds', glob.glob('worlds/*.world')),
        ('share/' + package_name + '/config', []),
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
