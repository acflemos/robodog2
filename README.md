# robodog2

Robô de vigilância doméstica com comportamento autônomo inspirado em cachorro — e cenário de **exploração espacial** em lava tube lunar para aprender ROS2, IA e robótica de forma interativa, com hardware acessível e uso em casa.

Migração do [robodog1](https://github.com/acflemos/robodog1) (ROS1 Noetic) para **ROS2 Humble** com hardware **ROSMASTER X3** da Yahboom.

---

## 🤖 Monitor de IA e Guia de Aprendizado (NotebookLM)

Para auxiliar no seu percurso de aprendizado, este projeto conta com um **Guia de Aprendizado Interativo** (Google NotebookLM). Através dele, você pode conversar com uma IA treinada na documentação do robodog2.

**Aceder ao guia:** [NotebookLM — robodog2](https://notebooklm.google.com/notebook/a48b8880-a5c9-4580-a2ab-3e82a9d156b8)

Com o guia, você pode:

- **Esclarecer dúvidas técnicas** sobre a integração do hardware ROSMASTER X3 com o ROS 2 Humble
- **Explorar a simulação** no Gazebo Fortress, incluindo detalhes sobre os plugins de odometria e os mundos de lava tubes
- **Estudar com materiais dinâmicos** — quizzes, flashcards, guias de referência e áudios explicativos sobre os "instintos" do robô

O contexto da IA é **limitado ao âmbito do projeto** e temas relacionados (ROS2, lava tube, Raspberry Pi, Jetson Nano, LiDAR, navegação autónoma, etc.). Serve como parceiro de estudos complementar a este repositório, não como substituto da documentação oficial do ROS2.

**Nota de segurança e privacidade:** ao acessar o link, você entra numa sessão de leitura individual. Suas perguntas e interações são privadas, não são visíveis para outros utilizadores e não alteram o conteúdo original do notebook. Use-o livremente como seu parceiro de estudos!

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
| Status | congelado — referência de código | em desenvolvimento ativo |

---

## Simulação Gazebo Fortress — o que o fabricante não fornece

O fabricante Yahboom **não fornece suporte a Gazebo** para o ROSMASTER X3. O robodog2 preenche essa lacuna com uma integração completa para ROS2 Humble + Gazebo Fortress:

- **URDF de simulação** com plugins Fortress (`ignition-gazebo-velocity-control`, `ignition-gazebo-odometry-publisher`, `ignition-gazebo-joint-state-publisher`, LiDAR `gpu_lidar`)
- **Bridge ROS–Gazebo** configurado via `ros_gz_bridge` (`/cmd_vel`, `/odom`, `/scan`, `/tf`, `/clock`)
- **Mundos SDF** convertidos de Gazebo Classic para Fortress (`cma_vazio.world`, `cma_moveis.world`)
- **SLAM funcional** com `slam_toolbox` — mapas gerados e versionados dentro do pacote
- **Nav2 + DWB + AMCL omni** em simulação, com tuning para ambiente doméstico
- **Navegação autónoma** com patrulha por pesos (`rbd2_navega`) — validada em simulação

---

## Lava tube lunar

Segundo ambiente do projeto: um **lava tube lunar** simulado em Gazebo Fortress (gravidade 1/6g), pensado para o mesmo stack ROS2 da casa simulada — SLAM, teleop, lidar, Nav2 — mas com narrativa de **exploração espacial** e habitats humanos sustentáveis na Lua e em Marte.

| | Casa simulada (`cma_moveis`) | Lava tube (`lava_tube`) |
|---|---|---|
| Onde corre | Gazebo + robô real em casa | Gazebo (gravidade lunar) |
| Papel | Aprender e replicar em casa | Mesmo conhecimento ROS2 com ambição espacial |
| Robô Fase 1 | ROSMASTER X3 (rodas) | ROSMASTER X3 — **zona navegável parcial** do túnel |
| Robô Fase 2 | — | **robodog3** (futuro: 4 pernas com rodas nas pontas) — exploração completa |

### Por que este cenário?

Lava tubes são túneis naturais candidatos a habitats lunares e marcianos (proteção contra radiação, temperatura estável, escala para instalações humanas). Antes de humanos entrarem, robôs autónomos mapeiam e inspecionam o interior — exactamente o que o curso ensina. Ver [docs/LAVA_TUBE.md](docs/LAVA_TUBE.md).

### O que o aluno faz (Fase 1 — robodog2)

1. Entra na boca do túnel (semi-enterrada na superfície lunar) com o X3.
2. Teleopera, usa o lidar e inicia os primeiros mapas na **porção navegável**.
3. Avança até o limite natural das rodas (subida do piso do túnel).
4. Avista ao longe a **zona do Enigma** — beacon emissivo, lander antigo, artefatos — e fica a pergunta: *quem esteve aqui antes?*
5. Para explorar o túnel completo (curva S, alcova, câmara), será preciso o **robodog3**.

Decisão técnica **v1.1** (documentada, implementação pendente): entrada semi-enterrada + rampa + subida progressiva do piso — ver [docs/PLANEJAMENTO_LAVA_TUBE.md](docs/PLANEJAMENTO_LAVA_TUBE.md).

### Como lançar

```bash
rbd2_build_pkg && rbd2_source
source ~/.bash_aliases

rbd_lava_tube        # túnel operacional (v1, piso plano; v1.1 em desenvolvimento)
rbd_lava_tube_fuel   # referência visual do interior rochoso (meshes Fuel DARPA SubT)
```

Branch de trabalho: `lava_tubes_grok`. Mundo gerado por `worlds/generate_lava_tube.py`.

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

## Status atual (2026-06-19)

### Validado ✅

- Robô ROSMASTER X3 spawnado em `cma_moveis.world` e `cma_vazio.world` sem flickering
- Teleop mecanum omnidirecional: frente/trás, strafe, rotação, diagonais
- `OdometryPublisher` publicando `/odom` e TF `odom→base_footprint`
- LiDAR `/scan` bridgado e funcional
- **SLAM funcional** — `rbd2_slam_x3_vazio` e `rbd2_slam_x3_moveis` geram mapas em tempo real
- **Mapas gerados e versionados** — `maps/rbd_mapa_vazio.yaml` e `maps/rbd_mapa_moveis.yaml` dentro do pacote
- **Nav2 + DWB funcional em simulação** — `rbd2_simulador_x3` e `rbd2_simulador_x3_moveis` arrancam sem erros
- **Navegação autónoma por goal**: Nav2 Goal → robô chega ao destino de forma eficiente
- RViz com `robodog2.rviz`: Nav2 panel, mapa, costmaps local/global, paths visíveis
- **`rbd2_navega` funcional em `cma_vazio.world`** — percorre toda a casa; `foge_de_parede()` resolve situações de canto
- **`rbd2_navega` funcional em `cma_moveis.world`** — navegação autónoma validada com tuning Nav2
- **Tuning Nav2 para `cma_moveis.world`** — `inflation_radius`, `cost_scaling_factor`, `sim_time`, `acc_lim_theta` e partículas AMCL ajustados
- Fix GLSL RViz em VM: `OGRE_RTT_MODE=Copy` em `~/.bash_aliases`

### Em progresso 🎯

- **Lava tube v1.1** — geometria de zona navegável parcial (entrada semi-enterrada, rampa, subida progressiva) em `generate_lava_tube.py`
- Testar código Yahboom original no Gazebo — comparar comportamento de navegação com robodog2
- Testar código robodog2 no robot real (`rbd2_bringup` no ROSMASTER X3 físico)

### Por fazer ❌

- Testar código Yahboom no robot real (X3 físico)
- Integrar Rosmaster ↔ robodog2 — cruzar o melhor dos dois códigos
- Calibração de `rbd_tabelas.py` para `cma_moveis.world`
- Ciclo autónomo em hardware físico

---

## Aliases (`~/.bash_aliases`)

### Workspace e build
```bash
alias rbd2_ws='cd ~/ros2_ws'
alias rbd2_build='cd ~/ros2_ws && colcon build'
alias rbd2_build_pkg='cd ~/ros2_ws && colcon build --packages-select robodog2'
alias rbd2_source='source ~/ros2_ws/install/setup.bash'
```

### Simulação Gazebo Fortress
```bash
# Mundo de teste vazio
alias rbd2_gz_x3='ros2 launch robodog2 rbd_gz_x3_launch.py'
alias rbd2_gz_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py rviz:=true'

# Casa com móveis (mundo de operação)
alias rbd2_casa_x3='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world'
alias rbd2_casa_x3_rviz='ros2 launch robodog2 rbd_gz_x3_launch.py world:=cma_moveis.world rviz:=true'

# Lava tube lunar (branch lava_tubes_grok) — ver docs/LAVA_TUBE.md
alias rbd_lava_tube='ros2 launch robodog2 rbd_lava_tube_launch.py'          # v1 operacional (caixa oca)
alias rbd_lava_tube_fuel='ros2 launch robodog2 rbd_lava_tube_fuel_launch.py' # referência visual Fuel
```

### SLAM — gerar mapas
```bash
# Casa vazia — mapa de referência geométrica
alias rbd2_slam_x3_vazio='ros2 launch robodog2 rbd_slam_x3_launch.py world:=cma_vazio.world'
alias rbd2_salva_mapa_vazio='ros2 run nav2_map_server map_saver_cli -f $RBD2_MAPS_SRC/rbd_mapa_vazio \
  && cp $RBD2_MAPS_SRC/rbd_mapa_vazio.{yaml,pgm} $(ros2 pkg prefix robodog2)/share/robodog2/maps/'

# Casa com móveis — mapa de operação real
alias rbd2_slam_x3_moveis='ros2 launch robodog2 rbd_slam_x3_launch.py world:=cma_moveis.world'
alias rbd2_salva_mapa_moveis='ros2 run nav2_map_server map_saver_cli -f $RBD2_MAPS_SRC/rbd_mapa_moveis \
  && cp $RBD2_MAPS_SRC/rbd_mapa_moveis.{yaml,pgm} $(ros2 pkg prefix robodog2)/share/robodog2/maps/'
```

> `$RBD2_MAPS_SRC` aponta para `~/ros2_ws/src/robodog2/maps/`. O alias salva o mapa lá e copia para o diretório de instalação do colcon para que o launch o encontre sem rebuild.

### Simulador completo e operação
```bash
# Casa vazia — Pré-requisito: maps/rbd_mapa_vazio.yaml gerado pelo rbd2_slam_x3_vazio
alias rbd2_simulador_x3='ros2 launch robodog2 rbd_simulador_x3_launch.py'

# Casa com móveis — Pré-requisito: maps/rbd_mapa_moveis.yaml gerado pelo rbd2_slam_x3_moveis
alias rbd2_simulador_x3_moveis='ros2 launch robodog2 rbd_simulador_x3_launch.py \
  world:=cma_moveis.world \
  map:=$(ros2 pkg prefix robodog2)/share/robodog2/maps/rbd_mapa_moveis.yaml'

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

# Terminal 2 — percorrer todos os cômodos com o teclado
rbd2_teclado

# Terminal 2 — quando o mapa estiver completo
rbd2_salva_mapa_vazio       # → maps/rbd_mapa_vazio.yaml + maps/rbd_mapa_vazio.pgm (no pacote)
```

### Gerar o mapa da casa com móveis
```bash
# Terminal 1
rbd2_slam_x3_moveis         # Gazebo + slam_toolbox + RViz

# Terminal 2
rbd2_teclado
rbd2_salva_mapa_moveis      # → maps/rbd_mapa_moveis.yaml (no pacote)
```

### Simulação autónoma — casa vazia
```bash
# Terminal 1
rbd2_simulador_x3           # Gazebo + Nav2 + AMCL + RViz (mapa: maps/rbd_mapa_vazio.yaml)

# Terminal 2
rbd2_navega                 # loop autónomo de patrulha por pesos
```

### Simulação autónoma — casa com móveis
```bash
# Terminal 1
rbd2_simulador_x3_moveis    # Gazebo + Nav2 + AMCL + RViz (mapa: maps/rbd_mapa_moveis.yaml)

# Terminal 2
rbd2_navega                 # loop autônomo de patrulha por pesos
```

### Exploração inicial — lava tube lunar
```bash
# Terminal 1
rbd_lava_tube               # Gazebo + robô na superfície lunar (branch lava_tubes_grok)

# Terminal 2 — teleop e primeiros mapas na zona navegável
rbd2_teclado
# SLAM: adaptar rbd_slam_x3_launch.py com world:=lava_tube.world quando validado
```

---

## Arquitetura de simulação (Gazebo Fortress)

```
rbd_gz_x3_launch.py
├── ign gazebo servidor (-r -s -v4)   ← mundo .world em worlds/
├── ign gazebo GUI (-g -v4)
├── robot_state_publisher             ← URDF: urdf/rbd_X3_sim.urdf.xacro
├── ros_gz_sim create                 ← spawn rosmaster_x3 em (-3.0, -2.0, 0.1)
└── ros_gz_bridge (parameter_bridge)  ← config: config/rbd_x3_bridge.yaml

rbd_simulador_x3_launch.py            ← default: cma_vazio.world + maps/rbd_mapa_vazio.yaml
├── rbd_gz_x3_launch.py               ← Gazebo Fortress (world configurável)
├── navigation_dwa_launch.py          ← Nav2: AMCL omni + DWB + BT Navigator + recoveries
│                                        params: params/rbd_dwa_nav_params.yaml
└── rviz2                             ← config: rviz/robodog2.rviz (Nav2 panel + costmaps)

rbd_slam_x3_launch.py
├── rbd_gz_x3_launch.py               ← Gazebo Fortress (world configurável)
├── async_slam_toolbox_node           ← params: params/rbd_slam_toolbox_params.yaml
└── rviz2                             ← config: rviz/map.rviz
```

**Plugins URDF ativos (Fortress v6):**
- `ignition-gazebo-velocity-control-system` → subscreve `/model/rosmaster_x3/cmd_vel`
- `ignition-gazebo-odometry-publisher-system` → publica `/odom` e TF `odom→base_footprint`
- `ignition-gazebo-joint-state-publisher-system` → publica `/joint_states`
- LiDAR `gpu_lidar` → publica `/scan`

**Bridge ativo (`rbd_x3_bridge.yaml`):**
- GZ→ROS: `/clock`, `/joint_states`, `/odom`, `/tf`, `/scan`
- ROS→GZ: `/cmd_vel` → `/model/rosmaster_x3/cmd_vel`

---

## Arquitetura de comportamento autônomo

```
rbd_tabelas.py   — pontos de destino, rotas, pesos de tarefas (dados estáticos)
rbd_md.py        — classes CASA, TAREFAS, ROBO
rbd_funcoes.py   — move_to_goal() via Nav2, leitura do laser scan
rbd_navega.py    — nó ROS2 principal: MultiThreadedExecutor + thread do loop
```

**Loop de seleção de tarefas por peso (instintos programados):**
1. A cada ciclo todos os pesos das tarefas ativas são incrementados
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

| Arquivo | Conteúdo | Status |
|---|---|---|
| `worlds/cma_vazio.world` | Casa sem móveis — 15 cômodos | ✅ Fortress |
| `worlds/cma_moveis.world` | Casa com móveis — 79 modelos | ✅ Fortress |
| `worlds/rbd_gz_empty.world` | Mundo vazio para testes | ✅ Fortress |
| `worlds/lava_tube.world` | Lava tube lunar (1/6g), túnel + câmara do Enigma; gerado por `generate_lava_tube.py` | 🎯 v1.1 em progresso (`lava_tubes_grok`) |
| `worlds/lava_tube_fuel.world` | Referência visual Fuel — interior rochoso; piso irregular, sem colisão para rodas | ✅ referência |

Os mundos `cma_*` foram convertidos de Gazebo Classic (SDF 1.6) para Fortress: poses dos modelos atualizadas a partir do bloco `<state>` do arquivo original. Detalhes do lava tube: [worlds/README.md](worlds/README.md).

---

## Mapas gerados

| Arquivo | Mundo | Resolução |
|---|---|---|
| `maps/rbd_mapa_vazio.yaml` | `cma_vazio.world` | 485×378 @ 0.05 m/px |
| `maps/rbd_mapa_moveis.yaml` | `cma_moveis.world` | 312×374 @ 0.05 m/px |

---

## Referências

- [docs/LAVA_TUBE.md](docs/LAVA_TUBE.md) — proposta pedagógica do lava tube
- [docs/PLANEJAMENTO_LAVA_TUBE.md](docs/PLANEJAMENTO_LAVA_TUBE.md) — fases técnicas, Enigma, decisão v1.1
- [robodog1](https://github.com/acflemos/robodog1) — versão ROS1 (congelada)
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3)
- [Nav2](https://navigation.ros.org/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [ROS2 Humble](https://docs.ros.org/en/humble/)
- [Ignition Gazebo / Fortress](https://gazebosim.org/docs/fortress)
