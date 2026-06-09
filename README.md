# robodog2

Robô de vigilância doméstica com comportamento autônomo inspirado em cachorro.

Migração do [robodog1](https://github.com/antoniocfl/robodog1) (ROS1 Noetic) para **ROS2 Humble** com hardware **ROSMASTER X3** da Yahboom.

---

## Contexto da migração

| | robodog1 | robodog2 |
|---|---|---|
| ROS | ROS1 Noetic | ROS2 Humble |
| Hardware | TurtleBot3 Waffle (simulado) + Arduino | ROSMASTER X3 (Raspberry Pi 4, Yahboom) |
| Simulação | Gazebo Classic | Gazebo Fortress (Ignition Gazebo v6.17.1) |
| Navegação | move_base | Nav2 |
| Build | catkin | colcon / ament_python |
| Status | congelado — referência de código | em desenvolvimento |

---

## Hardware

**ROSMASTER X3 — Yahboom**
- Raspberry Pi 4B (4GB)
- LiDAR 360° (LDROBOT LD14)
- Câmera RGB
- Rodas mecanum omnidirecionais
- Firmware: pacotes `yahboomcar_*` em ROS2

---

## Ambiente de desenvolvimento

- Ubuntu 22.04, ROS2 Humble
- Gazebo Fortress v6.17.1 (`ign gazebo`)
- Workspace principal: `~/ros2_ws/`
- Branch activa de desenvolvimento: `fix/rbd2_casa_x3_claude`

---

## Aliases activos (`~/.bash_aliases`)

### Build e workspace
```bash
alias rbd2_build_pkg='cd ~/ros2_ws && colcon build --packages-select robodog2'
alias rbd2_source='source ~/ros2_ws/install/setup.bash'
alias rbd2_ws='cd ~/ros2_ws'
alias gemini_ws='cd ~/workspace_gemini'
alias source_gemini='source /opt/ros/humble/setup.bash && source ~/workspace_gemini/install/setup.bash'
alias source_ros2ws='source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash'
```

### Simulação Gazebo Fortress (em desenvolvimento activo)
```bash
# Mundo vazio — teste base do robô
alias rbd2_gz_x3='ros2 launch robodog2 rbd_gz_x3_launch.py'

# Mundo da casa com móveis — alias principal da branch fix/rbd2_casa_x3_claude
alias rbd2_casa_x3='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world'

# Com RViz2
alias rbd2_casa_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world rviz:=true'
```

### SLAM e mapeamento
```bash
alias rbd2_slam_x3='ros2 launch robodog2 rbd_slam_x3_launch.py'
alias rbd2_salva_mapa_moveis='ros2 run nav2_map_server map_saver_cli -f ~/rbd_mapa_moveis'
```

### Simulação completa com Nav2
```bash
# Pré-requisito: ~/rbd_mapa_moveis.yaml gerado via rbd2_slam_x3
alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py'
```

### Teleoperação e hardware
```bash
alias rbd2_teclado='ros2 run teleop_twist_keyboard teleop_twist_keyboard'
alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py'
alias rbd2_navega='ros2 run robodog2 rbd_navega'
```

---

## Arquitetura de simulação (Gazebo Fortress)

```
rbd_gz_x3_launch.py
├── ign gazebo (servidor + GUI)        ← mundo .world em worlds/
├── robot_state_publisher              ← URDF: urdf/rbd_X3_sim.urdf.xacro
├── ros_gz_sim create                  ← spawn do robô no mundo
├── ros_gz_bridge (parameter_bridge)   ← config: config/rbd_x3_bridge.yaml
└── rviz2 (opcional)
```

**Plugins activos no URDF (Fortress v6):**
- `ignition-gazebo-velocity-control-system` → subscreve `/model/rosmaster_x3/cmd_vel`
- `ignition-gazebo-odometry-publisher-system` → publica `/odom` e `/tf`
- `ignition-gazebo-joint-state-publisher-system` → publica `/joint_states`
- LiDAR `gpu_lidar` → publica `/scan`

**Bridge activo (`rbd_x3_bridge.yaml`):**
- `/clock`, `/joint_states`, `/odom`, `/tf`, `/scan` (GZ→ROS)
- `/cmd_vel` (ROS→GZ via `/model/rosmaster_x3/cmd_vel`)

---

## Status da branch `fix/rbd2_casa_x3_claude`

### Validado ✅
- Robô ROSMASTER X3 spawnado em `cma_moveis.world` sem flickering
- Teleop mecanum omnidirecional: frente/trás, strafe, rotação, diagonais
- `OdometryPublisher` a publicar `/odom` e TF `odom→base_footprint`
- `JointStatePublisher` activo
- LiDAR `/scan` bridgado
- Terminal sem erros críticos (apenas warnings Qt do Gazebo GUI — inofensivos)

### Em progresso ⚠️
- TF chain completa para RViz (`map→odom→base_footprint→base_link`)
- `rbd2_simulador_x3` — Nav2 + AMCL + bt_navigator

### Por fazer ❌
- SLAM para gerar mapa com hardware actual
- Navegação autónoma validada em simulação
- `rbd2_bringup` no ROSMASTER X3 real
- Calibração dos pontos de destino `rbd_tabelas.py` para `cma_moveis.world`

---

## Arquitectura de comportamento autónomo

```
rbd_tabelas.py   — dados estáticos: 74 pontos de destino, 19 rotas, pesos de tarefas
rbd_md.py        — modelo de domínio: classes CASA, TAREFAS, ROBO
rbd_funcoes.py   — navegação: move_to_goal() via Nav2, leitura do laser scan
rbd_navega.py    — nó ROS2 principal: MultiThreadedExecutor + thread do loop
```

---

## Dependências

```bash
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-ros-gz \
  ros-humble-imu-filter-madgwick \
  ros-humble-slam-toolbox
```

---

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select robodog2
source install/setup.bash
```

---

## Referências

- [robodog1](https://github.com/antoniocfl/robodog1) — versão ROS1 (congelada)
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3)
- [Nav2](https://navigation.ros.org/)
- [ROS2 Humble](https://docs.ros.org/en/humble/)
- [Ignition Gazebo / Fortress](https://gazebosim.org/docs/fortress)
