# robodog2

Robô de vigilância doméstica com comportamento autônomo inspirado em cachorro.

Migração do [robodog1](https://github.com/acflemos/robodog1) (ROS1 Noetic) para **ROS2 Humble** com hardware **ROSMASTER X3** da Yahboom.

---

## Contexto da migração

| | robodog1 | robodog2 |
|---|---|---|
| ROS | ROS1 Noetic | ROS2 Humble |
| Hardware | TurtleBot3 Waffle (simulado) + Arduino | ROSMASTER X3 (Raspberry Pi 4, Yahboom) |
| Simulação | Gazebo Classic | Gazebo Fortress (Ignition Gazebo v6.17.1) |
| Navegação | move_base + AMCL | Nav2 (AMCL omni + DWB) |
| SLAM | gmapping | slam_toolbox |
| Build | catkin | colcon / ament_python |
| Status | congelado — referência de código | em desenvolvimento activo |

---

## Hardware

**ROSMASTER X3 — Yahboom**
- Raspberry Pi 4B (4 GB)
- LiDAR 360° (YDLIDAR X4 / LDROBOT LD14)
- Câmera RGB
- IMU (hardware real — não usado em simulação)
- Rodas mecanum (omnidirecionais)

---

## Ambiente de desenvolvimento

- Ubuntu 22.04, ROS2 Humble
- Gazebo Fortress v6.17.1 (`ign gazebo`) — **NÃO é Gazebo Harmonic**
- Workspace principal: `~/ros2_ws/`

---

## Status actual (2026-06-15)

### Validado ✅

- Robô ROSMASTER X3 spawnado em `cma_moveis.world` e `cma_vazio.world` sem flickering
- Teleop mecanum omnidirecional: frente/trás, strafe, rotação, diagonais
- `OdometryPublisher` publicando `/odom` e TF `odom→base_footprint`
- LiDAR `/scan` bridgado e funcional
- **SLAM funcional** — `rbd2_slam_x3_vazio` gera mapa em tempo real
- **Mapa da casa vazia gerado e guardado:** `~/rbd_mapa_vazio.yaml` (485×378 @ 0.05 m/px)
- **Nav2 + DWB funcional em simulação** — `rbd2_simulador_x3` arranca sem erros
- **Navegação autónoma por goal**: Nav2 Goal → robô chega ao destino de forma eficiente
- RViz com `robodog2.rviz`: Nav2 panel, mapa, costmaps local/global, paths visíveis

### Em progresso ⚠️

- `rbd2_navega` — loop autónomo de patrulha (Nav2 funcionou, pronto para testar)
- Calibração de `rbd_tabelas.py` — pontos de destino precisam ser ajustados para `cma_vazio.world`

### Por fazer ❌

- Mapa da casa com móveis (`rbd2_slam_x3_moveis`)
- Navegação autónoma validada em simulação (`rbd2_navega`)
- Calibração completa dos pontos de destino para a casa simulada
- `rbd2_bringup` no ROSMASTER X3 real
- Ciclo autónomo em hardware físico

---

## Aliases (`~/.bash_aliases`)

### Workspace e build
```bash
alias rbd2_ws='cd ~/ros2_ws'
alias rbd2_build='cd ~/ros2_ws && colcon build'
alias rbd2_build_pkg='cd ~/ros2_ws && colcon build --packages-select robodog2'
alias rbd2_source='source ~/ros2_ws/install/setup.bash'
alias source_ros2ws='source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash'
alias source_gemini='source /opt/ros/humble/setup.bash && source ~/workspace_gemini/install/setup.bash'
alias gemini_ws='cd ~/workspace_gemini'
```

### Simulação Gazebo Fortress
```bash
# Mundo vazio de teste
alias rbd2_gz_x3='ros2 launch robodog2 rbd_gz_x3_launch.py'
alias rbd2_gz_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py rviz:=true'

# Casa vazia (referência geométrica para pontos de destino)
alias rbd2_casa_x3='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world'
alias rbd2_casa_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world rviz:=true'

# Casa com móveis (mundo de operação)
alias rbd2_casa_x3_moveis='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world'
alias rbd2_casa_x3_moveis_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world rviz:=true'
```

### SLAM — gerar mapas
```bash
# Casa vazia — mapa de referência geométrica
alias rbd2_slam_x3_vazio='ros2 launch robodog2 rbd_slam_x3_launch.py'
alias rbd2_salva_mapa_vazio='ros2 run nav2_map_server map_saver_cli -f ~/rbd_mapa_vazio'

# Casa com móveis — mapa de operação real
alias rbd2_slam_x3_moveis='ros2 launch robodog2 rbd_slam_x3_launch.py world:=cma_moveis.world'
alias rbd2_salva_mapa_moveis='ros2 run nav2_map_server map_saver_cli -f ~/rbd_mapa_moveis'
```

### Simulador completo e operação
```bash
# Pré-requisito: ~/rbd_mapa_vazio.yaml ou ~/rbd_mapa_moveis.yaml
alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py'
alias rbd2_teclado='ros2 run teleop_twist_keyboard teleop_twist_keyboard'
alias rbd2_navega='ros2 run robodog2 rbd_navega'
alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py'
```

---

## Fluxos de uso

### Gerar o mapa da casa vazia (referência para `rbd_tabelas.py`)
```bash
# Terminal 1
rbd2_slam_x3_vazio          # Gazebo + slam_toolbox + RViz

# Terminal 2 — percorrer todos os cômodos
rbd2_teclado

# Terminal 2 — quando o mapa estiver completo
rbd2_salva_mapa_vazio       # → ~/rbd_mapa_vazio.yaml + ~/rbd_mapa_vazio.pgm
```

### Gerar o mapa da casa com móveis
```bash
# Terminal 1
rbd2_slam_x3_moveis         # Gazebo + slam_toolbox + RViz

# Terminal 2
rbd2_teclado
rbd2_salva_mapa_moveis      # → ~/rbd_mapa_moveis.yaml
```

### Simulação autónoma (mapa já existe)
```bash
# Terminal 1
rbd2_simulador_x3           # Gazebo + Nav2 + AMCL + RViz

# Terminal 2
rbd2_navega                 # loop autónomo de patrulha por pesos
```

---

## Arquitectura de simulação (Gazebo Fortress)

```
rbd_gz_x3_launch.py
├── ign gazebo servidor (-r -s -v4)   ← mundo .world em worlds/
├── ign gazebo GUI (-g -v4)
├── robot_state_publisher             ← URDF: urdf/rbd_X3_sim.urdf.xacro
├── ros_gz_sim create                 ← spawn rosmaster_x3 em (-3.0, -2.0, 0.1)
└── ros_gz_bridge (parameter_bridge)  ← config: config/rbd_x3_bridge.yaml

rbd_simulador_x3_launch.py
├── rbd_gz_x3_launch.py               ← Gazebo Fortress (world configurável)
├── navigation_dwa_launch.py          ← Nav2: AMCL omni + DWB + BT Navigator + recoveries
│                                        params: params/rbd_dwa_nav_params.yaml
└── rviz2                             ← config: rviz/robodog2.rviz (Nav2 panel + costmaps)

rbd_slam_x3_launch.py
├── rbd_gz_x3_launch.py               ← Gazebo Fortress (world configurável)
├── async_slam_toolbox_node           ← params: params/rbd_slam_toolbox_params.yaml
└── rviz2                             ← config: rviz/map.rviz
```

**Plugins URDF activos (Fortress v6):**
- `ignition-gazebo-velocity-control-system` → subscreve `/model/rosmaster_x3/cmd_vel`
- `ignition-gazebo-odometry-publisher-system` → publica `/odom` e TF `odom→base_footprint`
- `ignition-gazebo-joint-state-publisher-system` → publica `/joint_states`
- LiDAR `gpu_lidar` → publica `/scan`

**Bridge activo (`rbd_x3_bridge.yaml`):**
- GZ→ROS: `/clock`, `/joint_states`, `/odom`, `/tf`, `/scan`
- ROS→GZ: `/cmd_vel` → `/model/rosmaster_x3/cmd_vel`

---

## Arquitectura de comportamento autónomo

```
rbd_tabelas.py   — pontos de destino, rotas, pesos de tarefas (dados estáticos)
rbd_md.py        — classes CASA, TAREFAS, ROBO
rbd_funcoes.py   — move_to_goal() via Nav2, leitura do laser scan
rbd_navega.py    — nó ROS2 principal: MultiThreadedExecutor + thread do loop
```

**Loop de selecção de tarefas por peso (instintos programados):**
1. A cada ciclo todos os pesos das tarefas activas são incrementados
2. A tarefa com maior peso é escolhida (desempate aleatório)
3. O robô percorre os pontos de destino do cômodo via Nav2
4. O peso da tarefa executada é decrementado (reduz prioridade)
5. Quando todos os pesos ficam negativos o ciclo é reiniciado

---

## Build e instalação

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/acflemos/robodog2.git
cd ~/ros2_ws
colcon build --packages-select robodog2
source install/setup.bash
```

**Dependências:**
```bash
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-ros-gz \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-teleop-twist-keyboard
```

---

## Mundos Gazebo

| Ficheiro | Conteúdo | Estado |
|---|---|---|
| `worlds/cma_vazio.world` | Casa sem móveis — 15 cômodos | ✅ Fortress |
| `worlds/cma_moveis.world` | Casa com móveis — 79 modelos | ✅ Fortress |
| `worlds/rbd_gz_empty.world` | Mundo vazio para testes | ✅ Fortress |

Os mundos foram convertidos de Gazebo Classic (SDF 1.6) para Fortress: poses dos modelos actualizadas a partir do bloco `<state>` do ficheiro original.

---

## Mapas gerados

| Ficheiro | Mundo | Resolução | Data |
|---|---|---|---|
| `~/rbd_mapa_vazio.yaml` | `cma_vazio.world` | 485×378 @ 0.05 m/px | 2026-06-10 |
| `~/rbd_mapa_moveis.yaml` | `cma_moveis.world` | — | por gerar |

---

## Referências

- [robodog1](https://github.com/acflemos/robodog1) — versão ROS1 (congelada)
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3)
- [Nav2](https://navigation.ros.org/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [ROS2 Humble](https://docs.ros.org/en/humble/)
- [Ignition Gazebo / Fortress](https://gazebosim.org/docs/fortress)
