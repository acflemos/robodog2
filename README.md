# robodog2

Robô de vigilância doméstica com comportamento autônomo inspirado em cachorro.

Migração do [robodog1](https://github.com/antoniocfl/robodog1) (ROS1 Noetic) para **ROS2 Humble** com hardware **ROSMASTER X3** da Yahboom.

---

## Contexto da migração

| | robodog1 | robodog2 |
|---|---|---|
| ROS | ROS1 Noetic | ROS2 Humble |
| Hardware | TurtleBot3 Waffle (simulado) + Arduino | ROSMASTER X3 (Raspberry Pi 4, Yahboom) |
| Navegação | move_base | Nav2 |
| Build | catkin | colcon / ament_python |
| Status | congelado — referência de código | em desenvolvimento |

O robodog2 aproveita:
- A **lógica de comportamento** do robodog1 (`rbd_tabelas`, `rbd_md`, `rbd_funcoes`, `rbd_navega`) — portada para ROS2 com correções de bugs
- Os **pacotes yahboomcar** do ROSMASTER X3 como base de hardware (bringup, controle, laser, navegação, SLAM)

---

## Hardware

**ROSMASTER X3 — Yahboom**
- Raspberry Pi 4B (4GB)
- LiDAR 360°
- Câmera RGB
- IMU
- Rodas omnidirecionais / diferencial
- Firmware: pacotes `yahboomcar_*` em ROS2

---

## Arquitetura de comportamento

O comportamento autônomo é construído em três camadas (herdadas do robodog1):

```
rbd_tabelas.py   — dados estáticos: 74 pontos de destino, 19 rotas, pesos de tarefas
rbd_md.py        — modelo de domínio: classes CASA, TAREFAS, ROBO
rbd_funcoes.py   — navegação: move_to_goal() via Nav2, leitura do laser scan
rbd_navega.py    — nó ROS2 principal: MultiThreadedExecutor + thread do loop
```

**Loop de seleção de tarefas (por peso):**
1. A cada ciclo todos os pesos das tarefas ativas são incrementados
2. A tarefa com maior peso é escolhida (desempate aleatório)
3. O robô percorre os pontos de destino do cômodo correspondente via Nav2
4. O peso da tarefa executada é decrementado (penalidade), reduzindo sua prioridade
5. Quando todos os pesos ficam negativos, o ciclo é reiniciado

Isso cria um padrão de patrulha cíclica por todos os cômodos, com prioridade configurável por cômodo.

---

## Estrutura do repositório

```
robodog2/
├── robodog2/
│   ├── rbd_tabelas.py      # pontos de destino, rotas, pesos (dados da casa)
│   ├── rbd_md.py           # classes CASA, TAREFAS, ROBO
│   ├── rbd_funcoes.py      # move_to_goal (Nav2), scan laser, gestão de pesos
│   └── rbd_navega.py       # nó ROS2 principal
├── launch/
│   └── rbd_bringup.launch.py
├── config/                 # parâmetros de navegação (Nav2)
├── maps/                   # mapas salvos (.yaml + .pgm)
├── urdf/                   # modelo do robô
├── rviz/                   # configurações RViz2
├── package.xml
└── setup.py
```

---

## Dependências

- ROS2 Humble
- Nav2 (`ros-humble-navigation2`, `ros-humble-nav2-bringup`)
- Pacotes yahboomcar do ROSMASTER X3 (a integrar no workspace)

```bash
sudo apt-get install -y ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-nav2-msgs
```

---

## Instalação e build

```bash
# clonar dentro do workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/antoniocfl/robodog2.git

# compilar
cd ~/ros2_ws
colcon build --packages-select robodog2
source install/setup.bash
```

---

## Uso

```bash
# iniciar o nó de comportamento autônomo
ros2 run robodog2 rbd_navega

# ou via launch
ros2 launch robodog2 rbd_bringup.launch.py
```

**Aliases úteis** (adicionar ao `~/.bash_aliases`):

```bash
alias rbd2_build='cd ~/ros2_ws && colcon build --packages-select robodog2'
alias rbd2_source='source ~/ros2_ws/install/setup.bash'
alias rbd2_navega='ros2 run robodog2 rbd_navega'
alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py'
alias rbd2_slam='ros2 launch robodog2 rbd_slam.launch.py'
alias rbd2_nav='ros2 launch robodog2 rbd_nav.launch.py'
alias rbd2_salva_mapa='ros2 run nav2_map_server map_saver_cli -f ~/rbd2_mapa'
alias rbd2_teclado='ros2 run teleop_twist_keyboard teleop_twist_keyboard'
```

---

## Status do projeto

- [x] Port da lógica de comportamento (rbd_tabelas, rbd_md, rbd_funcoes, rbd_navega)
- [x] Integração com Nav2 (NavigateToPose action)
- [x] Correção de bugs de gestão de pesos do robodog1
- [x] Repositório GitHub criado (privado): https://github.com/acflemos/robodog2

### Próximas etapas (em ordem)

1. **Criar branch de desenvolvimento** — todas as próximas alterações em branch separada, nunca direto na main
2. **Documentar o ROSMASTER X3** — abrir `~/codigo_referencia/Rosmaster-x3/` no VS Code, comentar todos os arquivos dos pacotes yahboomcar e criar um README de referência para o projeto Rosmaster
3. **Escolher pacotes essenciais para navegação** — a partir da documentação gerada, selecionar os pacotes mínimos para fazer o robodog2 navegar no mapa do robodog1 (mundo simulado)
4. **Integrar pacotes yahboomcar no workspace** — copiar/linkar os pacotes selecionados para `~/ros2_ws/src/` e integrar com o launch do robodog2
5. **Validar navegação no mundo do robodog1** — testar o ciclo completo: bringup → mapa → Nav2 → rbd_navega
6. **Migrar etapas restantes gradativamente** — SLAM, mapa real da casa, calibração dos PDs, testes no hardware físico

- [ ] Branch de desenvolvimento criada
- [ ] Documentação dos pacotes yahboomcar gerada
- [ ] Pacotes essenciais selecionados para navegação
- [ ] Integração dos pacotes yahboomcar (bringup, base_node, laser, description)
- [ ] Launch file de SLAM com mapa da casa
- [ ] Launch file de navegação autônoma completo
- [ ] Mapa da casa calibrado para o ROSMaster X3
- [ ] Calibração dos pontos de destino (PD) para o novo hardware
- [ ] Testes no hardware físico

---

## Referências

- [robodog1](https://github.com/antoniocfl/robodog1) — versão ROS1 (congelada), base de código deste projeto
- [ROSMASTER X3 — Yahboom](https://github.com/YahboomTechnology/ROSMASTERX3) — pacotes yahboomcar de referência
- [Nav2](https://navigation.ros.org/) — stack de navegação ROS2
- [ROS2 Humble](https://docs.ros.org/en/humble/)
