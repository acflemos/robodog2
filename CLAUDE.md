# CLAUDE.md — robodog2

Contexto do projecto para o Claude Code. Lido automaticamente em qualquer máquina onde o repositório for clonado.

---

## O que é este projecto

Robô de vigilância doméstica com comportamento autónomo inspirado em cão, e cenário de exploração de **lava tube lunar** — tudo como base de um **curso de ROS2 em português**.

- Migração do robodog1 (ROS1 Noetic, congelado) para **ROS2 Humble**
- Hardware: **ROSMASTER X3** da Yahboom (Raspberry Pi 4B 8 GB, rodas mecanum)
- Simulação: **Gazebo Fortress v6.17.1** (`ign gazebo`) — **NÃO é Gazebo Harmonic**
- GitHub: https://github.com/acflemos/robodog2
- Utilizador GitHub: `acflemos`

---

## Objectivo educativo

Este projecto é a base de um **curso de ROS2 em português**. Isso afecta todas as decisões de código:

- Clareza e legibilidade acima de optimizações obscuras
- Comentários e nomes de variáveis em português onde for pedagogicamente claro
- Sem "magic numbers" — cada parâmetro deve ser compreensível
- Pensar sempre: *"um estudante de ROS2 consegue perceber o que este código faz?"*

---

## Ambiente

### PC de desenvolvimento
- Ubuntu 22.04, ROS2 Humble
- Gazebo Fortress v6.17.1 (`ign gazebo`) — plugin naming: `ignition-gazebo-*` / `ignition::gazebo::systems::*`
- Workspace: `~/ros2_ws/`
- Fix RViz em VM: `export OGRE_RTT_MODE=Copy` em `~/.bash_aliases`

### Robô físico (ROSMASTER X3)
- Raspberry Pi 4B, 8 GB RAM
- ROS2 Humble dentro de **container Docker**
- LiDAR: RPLIDAR A1 (driver: `sllidar_ros2`, porta `/dev/ttyUSB0`, publica `/scan`)
- IMU: MPU6050 (fusão Madgwick + EKF)
- Claude Code corre no **host do Pi** (fora do container); usa `docker exec` para correr comandos ROS2

### Pacotes no workspace (`~/ros2_ws/src/`)
```
robodog2/            ← este pacote (git próprio, GitHub)
yahboomcar_bringup/  ← bringup X3 (ficheiros modificados SEM git próprio)
yahboomcar_description/ ← URDF real (ficheiros modificados SEM git próprio)
yahboomcar_laser/    ← utilitários laser
yahboomcar_nav/      ← navegação Yahboom (ficheiros modificados SEM git próprio)
```

Os pacotes `yahboomcar_*` têm ficheiros modificados que **não estão em nenhum git**. Referência original: `/home/antonio/codigo_referencia/Rosmaster-x3/src/` (read-only, nunca modificar).

---

## Estrutura do pacote

```
robodog2/
  robodog2/
    rbd_navega.py      ← nó ROS2 principal (MultiThreadedExecutor + loop de patrulha)
    rbd_funcoes.py     ← move_to_goal() via Nav2, scan_retorno, foge_de_parede()
    rbd_md.py          ← classes CASA, TAREFAS, ROBO
    rbd_tabelas.py     ← pontos de destino, rotas, pesos (dados estáticos)
  launch/
    rbd_gz_x3_launch.py          ← Gazebo Fortress + bridge ROS-GZ
    rbd_slam_x3_launch.py        ← SLAM (world configurável)
    rbd_simulador_x3_launch.py   ← simulação completa: Gazebo + Nav2 + RViz
    navigation_dwa_launch.py     ← Nav2 interno (incluído pelos simuladores)
    rbd_robo_hardware_launch.py  ← hardware real: yahboomcar bringup + RPLIDAR A1
    rbd_bringup.launch.py        ← Nav2 real + RViz e navega opcionais
    rbd_lava_tube_launch.py      ← lava tube (Gazebo + gravidade lunar)
    rbd_lava_tube_fuel_launch.py ← lava tube com meshes Fuel (visual)
  params/
    rbd_dwa_nav_params.yaml      ← Nav2 para SIMULAÇÃO (use_sim_time: true)
    rbd_dwa_nav_params_real.yaml ← Nav2 para HARDWARE REAL (use_sim_time: false)
    rbd_slam_toolbox_params.yaml ← SLAM toolbox
  worlds/
    cma_vazio.world      ← casa sem móveis (15 cômodos)
    cma_moveis.world     ← casa com móveis (79 modelos)
    lava_tube.world      ← lava tube lunar v1.1 (gerado por generate_lava_tube.py)
    lava_tube_fuel.world ← referência visual com meshes Fuel DARPA SubT
    generate_lava_tube.py ← script Python que gera lava_tube.world
  maps/
    rbd_mapa_vazio.yaml / .pgm   ← mapa gerado com SLAM (versionado)
    rbd_mapa_moveis.yaml / .pgm  ← mapa gerado com SLAM (versionado)
  config/
    rbd_x3_bridge.yaml   ← bridge ROS↔Gazebo: /cmd_vel, /odom, /scan, /tf, /clock
  urdf/
    rbd_X3_sim.urdf.xacro ← URDF de simulação (plugins Fortress, odom 10 Hz)
  rviz/
    robodog2.rviz        ← Nav2 panel + costmaps + TF + scan
    map.rviz             ← SLAM (LaserScan verde 4px)
  docs/
    LAVA_TUBE.md              ← proposta pedagógica do lava tube
    PLANEJAMENTO_LAVA_TUBE.md ← fases técnicas, Enigma, decisão v1.1
```

---

## Arquitectura — Simulação

```
rbd_simulador_x3_launch.py
├── rbd_gz_x3_launch.py        ← Gazebo Fortress + spawn X3 em (-3.0, -2.0, 0.1)
│   └── ros_gz_bridge          ← config/rbd_x3_bridge.yaml
├── navigation_dwa_launch.py   ← Nav2 (use_sim_time=true)
│                                 params: params/rbd_dwa_nav_params.yaml
└── rviz2                      ← rviz/robodog2.rviz
```

**Plugins URDF Fortress:** `velocity-control`, `odometry-publisher` (10 Hz), `joint-state-publisher`, `gpu_lidar`

---

## Arquitectura — Robô Real

```
rbd_robo_hardware_launch.py         ← corre NO ROBÔ (container Docker)
├── yahboomcar_bringup_X3_launch.py
│   ├── Mcnamu_driver_X3            → /imu/data_raw, /vel_raw, /joint_states
│   ├── base_node_X3                → /odom
│   ├── imu_filter_madgwick         → /imu/data
│   ├── ekf (robot_localization)    → TF odom→base_footprint
│   └── robot_state_publisher       ← yahboomcar_X3.urdf
└── sllidar_launch.py               → /scan (RPLIDAR A1, /dev/ttyUSB0)

rbd_bringup.launch.py               ← PC ou robô (rede ROS2)
├── navigation_dwa_launch.py        ← Nav2 (use_sim_time=false)
│                                      params: params/rbd_dwa_nav_params_real.yaml
├── rviz2          (rviz:=true)     ← opcional
└── rbd_navega     (navega:=true)   ← opcional
```

**Nota importante:** no robô real, `set_initial_pose: false` — o operador define a pose com "2D Pose Estimate" no RViz2 antes de navegar.

---

## Fluxo de trabalho no robô físico

```bash
# Host do Pi (fora do container) — Claude Code corre aqui
docker exec -it <container> bash   # entrar no container para comandos ROS2

# Dentro do container
colcon build --packages-select robodog2 && source install/setup.bash
rbd2_robo_hardware    # Terminal 1: drivers + lidar

# PC ou robô (com mesmo ROS_DOMAIN_ID na rede)
rbd2_bringup_rviz     # Terminal 2: Nav2 + RViz
rbd2_navega           # Terminal 3: patrulha autónoma (opcional)
```

---

## Regras de trabalho com git

- **Branch por feature** — nunca commitar directamente em `main`
- **Nome da branch**: `snake_case` descritivo (ex: `bringup_robo_real`, `lava_tubes_grok`)
- **Commits**: `tipo(escopo): descrição em português` (feat, fix, docs, refactor)
- **PR antes de merge** — o utilizador revê e faz merge; Claude não faz merge directamente
- **Push**: só após o utilizador confirmar que os testes passaram
- No container do Pi: git configurado dentro do container; commit e push de dentro do container

---

## Convenções de código

- Ficheiros Python: prefixo `rbd_` (ex: `rbd_navega.py`, `rbd_funcoes.py`)
- Launch files: sufixo `_launch.py`
- Params YAML: prefixo `rbd_`
- Aliases bash: prefixo `rbd2_` (ex: `rbd2_simulador_x3`, `rbd2_bringup`)
- Mundos Gazebo: sem prefixo, nome descritivo (ex: `cma_vazio.world`, `lava_tube.world`)

---

## Estado actual (2026-07-14)

### Validado ✅
- Simulação completa: Gazebo Fortress + Nav2 + SLAM + patrulha autónoma
- Mundos: `cma_vazio.world`, `cma_moveis.world`, `lava_tube.world`, `lava_tube_fuel.world`
- Mapas versionados: `maps/rbd_mapa_vazio.yaml`, `maps/rbd_mapa_moveis.yaml`
- Navegação autónoma (`rbd2_navega`) validada em ambos os mundos da casa
- Lava tube v1.1: entrada semi-enterrada, rampa, zona do Enigma (PR #21 merged)
- Stack para hardware real criado (PR #22 merged): `rbd_robo_hardware_launch.py` + `rbd_dwa_nav_params_real.yaml` + `rbd_bringup.launch.py` actualizado

### Em progresso 🎯
- Testar `rbd2_robo_hardware` no ROSMASTER X3 físico (container Docker no Pi)
- Validar Nav2 real: localização AMCL + DWB com RPLIDAR A1 e odometria EKF

### Por fazer ❌
- SLAM da casa real → gerar mapa físico (ver estratégia de pose inicial abaixo)
- Calibrar `rbd_tabelas.py` para a casa real (waypoints do robô físico)
- Testar ciclo autónomo completo (`rbd2_navega`) no hardware físico
- Lava tube: SLAM + Nav2 na zona navegável
- Imagem Docker do robodog2 para distribuição do curso

---

## Estratégia de pose inicial — simulação ↔ mundo real

**Objectivo:** o robô físico começa sempre no mesmo ponto da casa, e o Nav2 sabe automaticamente onde está — sem intervenção manual no RViz. Reproduz no mundo real o que foi previsto na simulação.

**Na simulação:** o X3 spawna em `(-3.0, -2.0, 0.1)` no `cma_vazio.world`. O Nav2 usa `set_initial_pose: true` com essas coordenadas.

**No robô real — plano em 3 passos:**

1. **Marcar o ponto de partida físico** — colocar fita adesiva no chão da casa no local onde o robô vai sempre começar (ex: canto da sala de estar). Este ponto deve ser sempre o mesmo.

2. **Gerar o mapa real** — com o robô nesse ponto marcado, fazer SLAM da casa:
   ```bash
   # Adaptar rbd_slam_x3_launch.py para hardware (sem Gazebo, use_sim_time=false)
   # Teleop por todos os cômodos → salvar mapa
   ```
   O ponto marcado ficará com coordenadas próximas de (0, 0) no mapa gerado (origem do SLAM).

3. **Activar pose inicial automática** — após identificar as coordenadas do ponto marcado no mapa, actualizar `params/rbd_dwa_nav_params_real.yaml`:
   ```yaml
   set_initial_pose: true
   initial_pose:
     x: <x_do_ponto_marcado>   # a preencher após SLAM real
     y: <y_do_ponto_marcado>   # a preencher após SLAM real
     z: 0.0
     yaw: 0.0                  # robô orientado sempre na mesma direcção
   ```

**Resultado:** `rbd2_bringup` lança e o Nav2 localiza o robô automaticamente. Sem "2D Pose Estimate" no RViz — plug and play.

---

## Próximos passos (sessão 2026-07-15)

```
1. Pi host: instalar Claude Code (npm install -g @anthropic-ai/claude-code)
2. Container: git clone robodog2 + colcon build + configurar git (user + token)
3. Testar rbd2_robo_hardware → verificar /scan e /odom publicados
4. Testar rbd2_bringup_rviz → Nav2 no ar (mapa provisório da simulação)
5. SLAM da casa real → mapa físico → activar pose inicial automática
6. Calibrar waypoints rbd_tabelas.py → ciclo autónomo no robô físico
```
