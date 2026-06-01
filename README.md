# robodog2

Robô de vigilância doméstica com comportamento autônomo inspirado em cachorro.

Migração do [robodog1](https://github.com/acflemos/robodog1) (ROS1 Noetic) para **ROS2 Humble** com hardware **ROSMASTER X3** da Yahboom.

---

## Contexto da migração

| | robodog1 | robodog2 |
|---|---|---|
| ROS | ROS1 Noetic | ROS2 Humble |
| Hardware | TurtleBot3 Waffle (simulado) + Arduino | ROSMASTER X3 (Raspberry Pi 4, Yahboom) |
| Navegação | move_base + AMCL | Nav2 (AMCL omni + DWB) |
| SLAM | gmapping | slam_toolbox |
| Build | catkin | colcon / ament_python |
| Status | congelado — referência de código | em desenvolvimento |

O robodog2 aproveita:
- A **lógica de comportamento** do robodog1 (`rbd_tabelas`, `rbd_md`, `rbd_funcoes`, `rbd_navega`) — portada para ROS2 com correções de bugs
- Os **pacotes yahboomcar** do ROSMASTER X3 como base de hardware e navegação

---

## Hardware

**ROSMASTER X3 — Yahboom**
- Raspberry Pi 4B (4 GB)
- LiDAR 360° (YDLIDAR X4 / LDROBOT LD14)
- Câmera RGB
- IMU
- Rodas mecanum (omnidirecionais)

---

## Arquitetura de comportamento

O comportamento autônomo é construído em três camadas (herdadas do robodog1):

```
rbd_tabelas.py   — dados estáticos: pontos de destino, rotas, pesos de tarefas
rbd_md.py        — modelo de domínio: classes CASA, TAREFAS, ROBO
rbd_funcoes.py   — navegação: move_to_goal() via Nav2, leitura do laser scan
rbd_navega.py    — nó ROS2 principal: MultiThreadedExecutor + thread do loop
```

**Loop de seleção de tarefas (por peso):**
1. A cada ciclo todos os pesos das tarefas ativas são incrementados
2. A tarefa com maior peso é escolhida (desempate aleatório)
3. O robô percorre os pontos de destino do cômodo correspondente via Nav2
4. O peso da tarefa executada é decrementado, reduzindo sua prioridade
5. Quando todos os pesos ficam negativos, o ciclo é reiniciado

Isso cria um padrão de patrulha cíclica por todos os cômodos, com prioridade configurável por cômodo.

---

## Estrutura do repositório

```
robodog2/
├── robodog2/                        # módulo Python principal
│   ├── rbd_tabelas.py               # pontos de destino, rotas, pesos
│   ├── rbd_md.py                    # classes CASA, TAREFAS, ROBO
│   ├── rbd_funcoes.py               # move_to_goal (Nav2), scan laser
│   └── rbd_navega.py                # nó ROS2 principal
├── launch/
│   ├── rbd_bringup.launch.py        # bringup inicial
│   ├── rbd_gazebo_launch.py         # Gazebo genérico (world e posição configuráveis)
│   ├── rbd_casa_x3_launch.py        # Gazebo + X3 em cma_moveis.world — equiv. rbd_casa_x3
│   ├── rbd_slam_x3_launch.py        # SLAM em simulação (slam_toolbox) — gera o mapa
│   └── rbd_simulador_x3_launch.py   # simulador completo: Gazebo + Nav2 + RViz
├── urdf/
│   ├── rbd_X3_sim.urdf.xacro        # URDF ROS2 do X3 para simulação Gazebo
│   └── yahboomcar_X3_sim.urdf.xacro # URDF original ROS1 (referência)
├── worlds/                          # mundos Gazebo (cma_moveis.world, turtlebot3_*, ...)
├── yahboomcar_description/          # geometria e meshes do X3
├── yahboomcar_bringup/              # drivers hardware, EKF, IMU filter, joystick
├── yahboomcar_nav/                  # Nav2, SLAM, parâmetros de navegação
│   ├── launch/                      # navigation_dwa, cartographer, gmapping, rtabmap...
│   ├── params/
│   │   ├── dwa_nav_params.yaml      # Nav2 DWB — hardware real
│   │   ├── rbd_sim_dwa_params.yaml  # Nav2 DWB — simulação (use_sim_time + pose inicial AMCL)
│   │   └── rbd_slam_toolbox_params.yaml  # slam_toolbox — simulação
│   └── maps/                        # mapas de exemplo do yahboomcar
└── yahboomcar_laser/                # nós autônomos de laser (avoidance, tracker, warning)
```

---

## Dependências

```bash
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-nav2-msgs \
  ros-humble-slam-toolbox \
  ros-humble-imu-filter-madgwick \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-teleop-twist-keyboard
```

---

## Instalação e build

```bash
# clonar dentro do workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/acflemos/robodog2.git

# compilar
cd ~/ros2_ws
colcon build --packages-select robodog2
source install/setup.bash
```

---

## Aliases

Arquivo `~/.bash_aliases` (já configurado):

```bash
# Workspace
alias rbd2_ws='cd ~/ros2_ws'
alias rbd2_build='cd ~/ros2_ws && colcon build'
alias rbd2_build_pkg='cd ~/ros2_ws && colcon build --packages-select robodog2'
alias rbd2_source='source ~/ros2_ws/install/setup.bash'

# Hardware real
alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py'
alias rbd2_navega='ros2 run robodog2 rbd_navega'

# Simulação Gazebo Harmonic — mundo vazio (rbd_gz_empty.world)
alias rbd2_gz_x3='ros2 launch robodog2 rbd_gz_x3_launch.py'
alias rbd2_gz_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py rviz:=true'

# Simulação Gazebo Harmonic — mundo da casa (cma_vazio.world)
alias rbd2_casa_x3='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world'
alias rbd2_casa_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world rviz:=true'

# Simulação Gazebo Harmonic — mundos de teste
alias rbd2_casa_x3_teste='ros2 launch robodog2 rbd_gz_x3_launch.py world:=turtlebot3_house.world'
alias rbd2_casa_x3_teste2='ros2 launch robodog2 rbd_gz_x3_launch.py world:=gz/cma_vazio_teste2.world'
# gz/cma_vazio_teste2.world: cópia do arquivo gerado pelo gz sdf (sem bloco <state> do Classic)

# Simulação — gerar o mapa (fazer uma única vez)
alias rbd2_slam_x3='ros2 launch robodog2 rbd_slam_x3_launch.py'          # Gazebo + slam_toolbox + RViz
alias rbd2_salva_mapa_moveis='ros2 run nav2_map_server map_saver_cli -f ~/rbd_mapa_moveis'

# Simulação — simulador completo com mapa pré-construído
alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py' # Gazebo + Nav2 + RViz

# Utilitários
alias rbd2_teclado='ros2 run teleop_twist_keyboard teleop_twist_keyboard'
alias rbd2_slam='ros2 launch robodog2 rbd_slam.launch.py'
alias rbd2_nav='ros2 launch robodog2 rbd_nav.launch.py'
alias rbd2_salva_mapa='ros2 run nav2_map_server map_saver_cli -f ~/rbd2_mapa'
```

---

## Fluxos de uso

### Simulação — gerar o mapa da casa (primeira vez)

```bash
rbd2_build_pkg && rbd2_source    # compilar e ativar

# Terminal 1
rbd2_slam_x3                     # Gazebo + slam_toolbox + RViz

# Terminal 2 — percorrer a casa até o mapa estar completo no RViz
rbd2_teclado

# Terminal 2 — guardar o mapa
rbd2_salva_mapa_moveis           # → ~/rbd_mapa_moveis.yaml
```

### Simulação — comportamento autônomo (mapa já existe)

```bash
# Terminal 1
rbd2_simulador_x3                # Gazebo + Nav2 + RViz

# Terminal 2
rbd2_navega                      # loop autônomo de patrulha
```

### Correspondência com os aliases do robodog1 (ROS1)

| robodog1 (ROS1) | robodog2 (ROS2) |
|---|---|
| `rbd_casa_x3` | `rbd2_casa_x3` |
| `rbd_simulador_x3` | `rbd2_simulador_x3` |
| `rbd_navega` | `rbd2_navega` |

---

## Cadeia de nós — simulação Gazebo

```
Gazebo plugin planar_move  →  /odom  +  TF odom→base_footprint
Gazebo plugin IMU          →  /imu/data_raw  →  imu_filter_madgwick  →  /imu/data
Gazebo plugin LiDAR        →  /scan
robot_state_publisher      →  TF base_footprint→base_link→{rodas, laser_link, imu_link}
slam_toolbox               →  /map  +  TF map→odom          (modo SLAM)
Nav2 AMCL                  →  TF map→odom                   (modo navegação com mapa)
Nav2 DWB                   →  /cmd_vel
```

---

## Bugs do robodog1 corrigidos no port

| Ficheiro | Bug | Fix |
|---|---|---|
| `rbd_md.py` | `TAREFAS.tarefa()` decrementava a lista global `rbd_tabelas` em vez de `self.pesos_tarefas` → decremento nunca tinha efeito | Decrementa diretamente `self.pesos_tarefas[itc]` |
| `rbd_md.py` | `TAREFAS.prioriza_tarefas()` não chamava `verifica_pesos_negativos()` → IndexError | Adicionado `verifica_pesos_negativos()` e chamada em `prioriza_tarefas()` |
| `yahboomcar_nav/params/dwa_nav_params.yaml` | `robot_model_type: "differential"` — errado para mecanum | Corrigido para `"omni"` |
| `yahboomcar_nav/params/teb_nav_params.yaml` | `robot_model_type: "differential"` + typo `ontroller_frequency` | Corrigido para `"omni"` e `controller_frequency` |
| `yahboomcar_nav/launch/laser_bringup_launch.py` | TF frame `"laser"` inconsistente com URDF | Corrigido para `"laser_link"` |
| `yahboomcar_laser/laser_Avoidance_a1_X3.py` | `self.Moving` não inicializado em `__init__` → AttributeError | Adicionado `self.Moving = False` |
| `yahboomcar_laser/laser_Tracker_4ROS.py` | `self.laserAngle` referenciado antes de ser definido → crash no primeiro scan | Renomeado para `self.LaserAngle` consistentemente |

---

## Status do projeto

- [x] Port da lógica de comportamento (rbd_tabelas, rbd_md, rbd_funcoes, rbd_navega)
- [x] Integração com Nav2 (NavigateToPose action, MultiThreadedExecutor)
- [x] Correção de bugs de gestão de pesos do robodog1
- [x] Importação e correção dos pacotes yahboomcar (bringup, nav, laser, description)
- [x] URDF ROS2 do X3 para simulação Gazebo (`rbd_X3_sim.urdf.xacro`)
- [x] Launch de simulação Gazebo genérico (`rbd_gazebo_launch.py`)
- [x] Launch da casa com móveis (`rbd_casa_x3_launch.py` — equiv. `rbd_casa_x3` do robodog1)
- [x] Launch de SLAM em simulação com slam_toolbox (`rbd_slam_x3_launch.py`)
- [x] Launch do simulador completo com Nav2 (`rbd_simulador_x3_launch.py` — equiv. `rbd_simulador_x3` do robodog1)
- [x] Parâmetros Nav2 para simulação (`rbd_sim_dwa_params.yaml`) com `use_sim_time` e pose inicial AMCL
- [x] Parâmetros slam_toolbox para simulação (`rbd_slam_toolbox_params.yaml`)

### Próximas etapas

1. **Corrigir mundo `cma_vazio.world`** — reconstruir manualmente no Gazebo Editor a partir do mundo vazio funcional; o arquivo gerado pelo `gz sdf` (em `worlds/gz/`) ainda apresenta paredes fora do lugar devido ao bloco `<state>` do Gazebo Classic
2. **Gerar o mapa** — executar `rbd2_slam_x3` + `rbd2_teclado`, guardar com `rbd2_salva_mapa_moveis`
3. **Testar ciclo completo em simulação** — `rbd2_simulador_x3` + `rbd2_navega`
4. **Calibrar pontos de destino (PD)** em `rbd_tabelas.py` para o mundo `cma_moveis.world`
5. **Migrar para hardware físico** — substituir `rbd_gazebo_launch.py` pelo bringup real

---

## Referências

- [robodog1](https://github.com/acflemos/robodog1) — versão ROS1 (congelada), base de código deste projeto
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3) — pacotes yahboomcar de referência
- [Nav2](https://navigation.ros.org/) — stack de navegação ROS2
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) — SLAM padrão Nav2 Humble
- [ROS2 Humble](https://docs.ros.org/en/humble/)
