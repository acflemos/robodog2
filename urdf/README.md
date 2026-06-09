# urdf/ — Modelos URDF do robodog (ROS1 → ROS2)

Esta pasta contém os arquivos URDF/Xacro que descrevem a geometria e os plugins de simulação do robodog. Os arquivos foram originados no projeto **robodog1 (ROS1)** e serão adaptados para **ROS2** como parte da migração.

---

## Estrutura e finalidade de cada arquivo

### Arquivo principal do robô

| Arquivo | Descrição |
|---|---|
| [rbd_turtlebot3_waffle3.urdf.xacro](rbd_turtlebot3_waffle3.urdf.xacro) | **Versão atual em uso.** Corpo retangular (0.40×0.32m), 4 rodas cilíndricas, LiDAR, 4 ultrassônicos e câmera RealSense R200. Inclui `rbd_common_properties.xacro` e `rbd_turtlebot3_waffle.gazebo2.xacro`. |
| [rbd_turtlebot3_waffle3.urdf 1.00.xacro](rbd_turtlebot3_waffle3.urdf%201.00.xacro) | Versão anterior 1.00 — três diferenças em relação à versão atual: (1) colisão da caixa mais alta (0.11m vs 0.07m); (2) raio de colisão das rodas maior (0.06m vs 0.051m); (3) **todos os 4 ultrassónicos partilham o mesmo joint origin do LiDAR** (`-0.064 0 0.122`), sendo separados apenas por offset visual — ao contrário da versão atual onde cada ultrassónico tem joint com posição física própria. |
| [rbd_turtlebot3_waffle3.urdf 1.01.xacro.xacro](rbd_turtlebot3_waffle3.urdf%201.01.xacro.xacro) | Versão anterior 1.01 — mesmas diferenças que a 1.00. |

### Plugins Gazebo (ROS1)

| Arquivo | Descrição |
|---|---|
| [rbd_turtlebot3_waffle.gazebo2.xacro](rbd_turtlebot3_waffle.gazebo2.xacro) | **Versão atual em uso.** Dois plugins `diff_drive` (rodas dianteiras e traseiras separadas), IMU (`libgazebo_ros_imu.so`), LiDAR 360° (0.12–3.5m, 5Hz), 4 sensores ultrassónicos (50Hz, 0.01–12m) e câmera de profundidade RealSense R200. |
| [rbd_turtlebot3_waffle.gazebo2 1.00.xacro](rbd_turtlebot3_waffle.gazebo2%201.00.xacro) | Versão 1.00 dos plugins — igual à atual. |
| [rbd_turtlebot3_waffle.gazebo2_1.01.xacro](rbd_turtlebot3_waffle.gazebo2_1.01.xacro) | Versão 1.01 dos plugins — igual à atual. |
| [turtlebot3_waffle.gazebo2.xacro](turtlebot3_waffle.gazebo2.xacro) | Versão experimental com plugin **mecanum drive** (`libmecanum_plugin.so`). Plugin `diff_drive` está comentado. Útil como referência para cinemática omnidirecional real no Gazebo. |
| [turtlebot3_waffle.gazebo2 1.00.xacro](turtlebot3_waffle.gazebo2%201.00.xacro) | Variante 1.00 com mecanum drive — igual à versão acima. |
| [turtlebot3_waffle.gazebo2 2.00.xacro](turtlebot3_waffle.gazebo2%202.00.xacro) | Variante 2.00 com mecanum drive. |

### URDF de simulação do ROSMASTER X3 (ROS1)

| Arquivo | Descrição |
|---|---|
| [yahboomcar_X3_sim.urdf.xacro](yahboomcar_X3_sim.urdf.xacro) | Descrição autônoma do ROSMASTER X3 com rodas mecanum para simulação. Usa `libgazebo_ros_planar_move.so` (movimento omnidirecional), LiDAR LDROBOT LD14 (0.12–12m, 360°, 6Hz) e IMU ICM20948. Malhas STL referenciadas em `package://robodog1/meshes/`. |

### Arquivo auxiliar de materiais

| Arquivo | Descrição |
|---|---|
| [rbd_common_properties.xacro](rbd_common_properties.xacro) | Define as cores/materiais reutilizáveis (`black`, `dark`, `blue`, `green`, `grey`, `orange`, `brown`, `red`, `white`). Incluído pelos arquivos `rbd_turtlebot3_waffle3.urdf.xacro` e suas variantes (1.00/1.01). **Nota:** `yahboomcar_X3_sim.urdf.xacro` define os seus materiais inline (Green, LightGray) sem incluir este ficheiro. |

---

## Topologia TF do robodog (ROS1)

```
map → odom → base_footprint → base_link
                                  ├── wheel_left_link_frente
                                  ├── wheel_right_link_frente
                                  ├── wheel_left_link
                                  ├── wheel_right_link
                                  ├── imu_link
                                  ├── base_scan          (LiDAR)
                                  ├── ultrasom_f_scan    (ultrassónico frente)
                                  ├── ultrasom_t_scan    (ultrassónico trás)
                                  ├── ultrasom_d_scan    (ultrassónico direita)
                                  ├── ultrasom_e_scan    (ultrassónico esquerda)
                                  └── camera_link
                                        ├── camera_rgb_frame → camera_rgb_optical_frame
                                        └── camera_depth_frame → camera_depth_optical_frame
```

---

## Adaptação para ROS2 (próximos passos)

- [ ] Substituir `$(find robodog1)/urdf/` por `$(find robodog2)/urdf/` nos includes
- [ ] Substituir `package://robodog1/meshes/` por `package://robodog2/meshes/` em `yahboomcar_X3_sim.urdf.xacro`
- [ ] Substituir plugins ROS1 (`libgazebo_ros_diff_drive.so`, `libgazebo_ros_imu.so`, `libgazebo_ros_laser.so`, `libgazebo_ros_range.so`) pelos equivalentes **ROS2** com parâmetros `ros__parameters`
- [ ] Usar `libgazebo_ros_planar_move.so` do `yahboomcar_X3_sim.urdf.xacro` como referência para o plugin omnidirecional no ROS2
- [ ] Avaliar se mantém rodas cilíndricas (robodog1) ou adota malhas STL mecanum (rosmaster X3)
