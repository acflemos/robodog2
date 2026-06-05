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

# Simulação Gazebo Harmonic — mundo da casa vazio (cma_vazio.world)
alias rbd2_casa_x3='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world'
alias rbd2_casa_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_vazio.world rviz:=true'

# Simulação Gazebo Harmonic — mundo da casa com móveis (cma_moveis.world)
alias rbd2_casa_x3_moveis='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world'
alias rbd2_casa_x3_moveis_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world rviz:=true'

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
Gazebo VelocityControl     →  controlo cinemático (linear.x/y + angular.z) — sem física de rodas
Gazebo OdometryPublisher   →  /odom  +  TF odom→base_footprint
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

## Mundos Gazebo — conversão Classic → Harmonic

### O problema do bloco `<state>`

Os mundos do robodog1 foram criados no **Gazebo Classic** (SDF 1.6). Quando o editor salva um arquivo `.world`, ele grava **dois conjuntos de poses** para cada modelo:

1. **Pose na definição `<model>`** — posição original de quando o modelo foi criado/importado
2. **Pose no bloco `<state>`** — posição real após qualquer movimentação no editor

O **Gazebo Classic** aplica o bloco `<state>` ao carregar o mundo, sobrescrevendo as poses originais. As paredes ficam nas posições corretas.

O **Gazebo Harmonic** não possui esse mecanismo: usa apenas a `<pose>` da definição `<model>`. Resultado: as paredes aparecem nas posições originais (erradas), frequentemente metros deslocadas.

**Exemplo concreto (`cma_escritorio`):**

| | x | y |
|---|---|---|
| Pose na definição (errada para Harmonic) | -7.395 | -4.04 |
| Pose no bloco `<state>` (posição real) | -1.797 | 1.021 |

### Solução adotada

Para cada modelo, substituir a `<pose>` da definição pela pose correspondente no bloco `<state>` do arquivo Classic. As poses relativas dos links dentro do modelo permanecem inalteradas.

Script de conversão: [`tools/convert_world_classic_to_harmonic.py`](tools/convert_world_classic_to_harmonic.py)

Para reutilizar com outro mundo:
1. Extrair as poses do bloco `<state>` do arquivo `.world` Classic:
   ```bash
   # O bloco <state> começa depois das definições de modelo e antes de </world>
   # Procurar: grep -n '<state\|</state>' arquivo.world
   ```
2. Atualizar `SRC`, `DST`, `STATE_POSES` e `MODEL_LINE_RANGES` no topo do script
3. Executar: `python3 tools/convert_world_classic_to_harmonic.py`

### Estado dos mundos

| Arquivo | Formato | Status |
|---|---|---|
| `worlds/robodog1_classic/cma_vazio.world` | SDF 1.6 Classic | Original de referência — não editar |
| `worlds/robodog1_classic/cma_moveis.world` | SDF 1.6 Classic | Original de referência — não editar |
| `worlds/cma_vazio.world` | SDF 1.8 Harmonic | ✅ Convertido — 15 cômodos, poses corretas |
| `worlds/cma_moveis.world` | SDF 1.8 Harmonic | ✅ Convertido — 79 modelos (paredes + 64 móveis), poses corretas, testado em 2026-06-04 |

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
- [x] `cma_vazio.world` convertido para Harmonic com poses corretas (15 cômodos)
- [x] `cma_moveis.world` convertido para Harmonic com poses corretas (79 modelos: paredes + 64 móveis)
- [x] Robô rosmaster_x3 aparece corretamente no mundo com móveis (testado 2026-06-04)
- [x] Teleop omnidirecional mecanum validado em Gazebo Harmonic (testado 2026-06-05)

### Marcos alcançados — simulação completa em Gazebo Harmonic

**2026-06-04** — Mundo com móveis validado:
```
rbd2_casa_x3_moveis   →  Gazebo Harmonic + cma_moveis.world + rosmaster_x3
```
O mundo carrega os 79 modelos (cômodos + 64 objetos de mobiliário) nas posições
corretas, herdadas do robodog1. O robô aparece no centro da sala de estar.

**2026-06-05** — Teleop mecanum omnidirecional validado:
```
rbd2_casa_x3_moveis + rbd2_teclado  →  todos os movimentos funcionais
```
Movimentos validados: frente/trás, strafe esquerda/direita, rotação horária/anti-horária,
diagonais, círculos. Plugin `MecanumDrive` substituído por `VelocityControl`
(controlo cinemático directo, equivalente ao `planar_move` do ROS1).

**Aviso esperado em simulação pura** (não é erro):
```
[imu_filter_madgwick]: Still waiting for data on topic imu/data_raw
```
O nó `imu_filter_madgwick` aguarda dados do IMU real. Em simulação, o tópico
`imu/data_raw` é publicado pelo bridge GZ→ROS mas pode demorar alguns segundos
a ter fluxo contínuo. Não afecta a navegação por teclado nem o SLAM.

### Próximas etapas

#### Fase 1 — Validar simulação completa (prioridade imediata)

1. **Visualização RViz** — `rbd2_casa_x3_moveis_rviz`: fazer aparecer o mapa de casa do laser scan (mapa do robodog1 ou novo via SLAM)
2. **Gerar o mapa** — executar `rbd2_slam_x3` + `rbd2_teclado`, percorrer todos os cômodos, guardar com `rbd2_salva_mapa_moveis`
3. **Ciclo completo de navegação** — `rbd2_simulador_x3` + `rbd2_navega` — validar que o robô visita pontos de destino autonomamente

#### Fase 2 — Ajustes de simulação

5. **Calibrar pontos de destino (PD)** em `rbd_tabelas.py` para o mundo `cma_moveis.world`
6. **DWB lateral** — configurar `max_vel_y` / `vy_samples` para aproveitar as rodas mecanum em simulação
7. **EKF com `vy`** — habilitar velocidade lateral no filtro de estado do robô

#### Fase 3 — Hardware físico

8. **Bringup real** (`rbd2_bringup`) — ligar o ROSMASTER X3 real e verificar tópicos
9. **Transferir mapa** — copiar `~/rbd_mapa_moveis.yaml` para o robô real
10. **Ciclo autónomo em hardware** — `rbd2_simulador_x3` equivalente no robô real

---

## Referências

- [robodog1](https://github.com/acflemos/robodog1) — versão ROS1 (congelada), base de código deste projeto
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3) — pacotes yahboomcar de referência
- [Nav2](https://navigation.ros.org/) — stack de navegação ROS2
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) — SLAM padrão Nav2 Humble
- [ROS2 Humble](https://docs.ros.org/en/humble/)
