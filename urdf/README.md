# urdf/

Modelos URDF/Xacro do ROSMASTER X3 para simulação em Gazebo Fortress.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [rbd_X3_sim.urdf.xacro](rbd_X3_sim.urdf.xacro) | Descrição do ROSMASTER X3 adaptada para ROS2 + Gazebo Fortress. Substitui `yahboomcar_X3_sim.urdf.xacro` (ROS1). |

## Plugins ativos (Gazebo Fortress v6)

| Plugin | Função |
|---|---|
| `ignition-gazebo-velocity-control-system` | Recebe `/model/rosmaster_x3/cmd_vel` e move o robô |
| `ignition-gazebo-odometry-publisher-system` | Publica `/odom` e TF `odom→base_footprint` a 10 Hz |
| `ignition-gazebo-joint-state-publisher-system` | Publica `/joint_states` |
| `gpu_lidar` | LiDAR 360° — publica `/scan` via bridge ROS-GZ |

## Topologia TF

```
map → odom → base_footprint → base_link
                                  ├── front_right_wheel
                                  ├── front_left_wheel
                                  ├── back_right_wheel
                                  ├── back_left_wheel
                                  └── lds_lfcd_sensor   (LiDAR)
```

## Malhas STL referenciadas

Todas em `meshes/mecanum/` e `meshes/sensor/`:

| Malha | Link |
|---|---|
| `mecanum/base_link_X3.STL` | Corpo principal |
| `mecanum/front_right_wheel_X3.STL` | Roda dianteira direita |
| `mecanum/front_left_wheel_X3.STL` | Roda dianteira esquerda |
| `mecanum/back_right_wheel_X3.STL` | Roda traseira direita |
| `mecanum/back_left_wheel_X3.STL` | Roda traseira esquerda |
| `sensor/laser_link.STL` | LiDAR |
| `sensor/camera_link.STL` | Câmera (visual apenas) |
