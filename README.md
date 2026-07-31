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

rbd_lava_tube        # túnel operacional (v1.1, zona navegável parcial)
rbd_lava_tube_fuel   # referência visual do interior rochoso (meshes Fuel DARPA SubT)
```

Branch de trabalho: `lava_tubes_grok`. Mundo gerado por `worlds/generate_lava_tube.py`.

---

## Hardware

**ROSMASTER X3 — Yahboom**
- Raspberry Pi 4B (8 GB RAM)
- LiDAR 360° RPLIDAR A1 (driver: `sllidar_ros2`, publica `/scan`)
- Câmera RGB
- IMU (MPU6050 — fusão Madgwick + EKF no bringup)
- Rodas mecanum (omnidirecionais)
- ROS2 Humble em container Docker

---

## Containers Docker no ROSMASTER X3 físico

O robô físico roda ROS2 dentro de um container Docker no Raspberry Pi. Existem dois containers relevantes:

| | Container original (Yahboom) | `robodog2_humble` (novo, em construção) |
|---|---|---|
| Imagem base | `yahboomtechnology/ros-foxy:4.0.5` | `ros:humble` |
| ROS | ROS2 Foxy | ROS2 Humble |
| Workspace | pacotes `yahboomcar_*` já "assados" na imagem, em `/root/yahboomcar_ros2_ws/yahboomcar_ws/src/` | `robodog2` + `yahboomcar_*` em `/home/rbd/ros2_ws/src/`, clonados via git |
| Gazebo / RViz | ❌ não tem — imagem de fábrica sem suporte a simulação | ✅ Gazebo Fortress (Ignition 6.18) + RViz2 instalados — permite rodar simulação e ferramentas gráficas dentro do próprio container do robô |
| Acesso a dispositivos USB | `--device` individual por dispositivo (`/dev/myserial`, `/dev/rplidar`, câmeras Astra, `/dev/video0`, `/dev/input`) | bind mount de **todo `/dev`** + `--privileged` — mais simples, cobre qualquer device automaticamente |
| `Rosmaster_Lib` (driver Python do Arduino) | já vem instalado (pacote proprietário Yahboom, instalado via `.egg`) | precisou ser instalado manualmente — **não existe no PyPI**; o código-fonte foi copiado do container original (`/root/yahboomcar_ros2_ws/software/py_install_V3.3.1/`) e instalado com `pip3 install pyserial .` |
| Uso pretendido | operação de fábrica Yahboom (app remoto, SLAM/nav próprios da Yahboom) | desenvolvimento e testes do robodog2 (Nav2, SLAM, patrulha autônoma) |

### Ligação física dos motores e do lidar (host → container)

O host (Raspberry Pi) tem regras `udev` em `/etc/udev/rules.d/usb.rules` que criam nomes fixos para os dispositivos USB seriais, independente de qual container é usado:

```
idVendor=1a86 idProduct=7523 (chip CH340, Arduino)  → symlink /dev/myserial → /dev/ttyUSB0
idVendor=10c4 idProduct=ea60 (chip CP210x, RPLIDAR) → symlink /dev/rplidar
```

`Rosmaster_Lib` abre `/dev/myserial` a 115200 baud por padrão — é essa a única via de comunicação com o Arduino que controla os motores mecanum.

**Atenção — conflito conhecido:** existe (ou existia) um programa de autostart no Pi (`Rosmaster/rosmaster/start_app.sh` → `rosmaster_main.py`, no container original) que escuta sinais do controle remoto. Pelo manual da Yahboom, esse programa **precisa ser fechado** (`kill_rosmaster.sh`) antes de subir qualquer container — ele também abre `/dev/myserial`, e só um processo pode manter essa porta serial aberta por vez. Se esse programa ainda estiver rodando em segundo plano, o `Rosmaster()` dentro do container vai falhar ou ter comportamento errático ao tentar abrir a porta.

### Passos para testar o robodog2 no hardware físico

1. ✅ **Confirmar que nada mais está segurando a porta serial** — checar se o programa de autostart do controle remoto não está rodando em segundo plano (`ps aux | grep -i rosmaster`, `lsof /dev/ttyUSB0`); encerrar com `kill_rosmaster.sh` se necessário.
2. ✅ **Ligar a placa expansora do X3** (alimenta o Arduino e o RPLIDAR).
3. ✅ **Subir o `robodog2_humble`** com bind mount de `/dev` + `--privileged` (garante acesso a `/dev/myserial` e `/dev/rplidar` automaticamente). Entre sessões o container fica parado — usar `docker start robodog2_humble`.
4. ✅ **Verificar os dispositivos dentro do container**: `ls -la /dev/myserial /dev/rplidar`.
5. ✅ **Testar a comunicação serial básica** antes de subir o ROS2:
   ```python
   from Rosmaster_Lib import Rosmaster
   car = Rosmaster()
   car.create_receive_threading()
   print(car.get_version(), car.get_battery_voltage())
   ```
   Validado em 2026-07-28: `Version: 3.3`, bateria em 11.5V.
6. ✅ **Compilar o workspace**: `colcon build --packages-select robodog2 && source install/setup.bash`
7. ✅ **Aplicar o fix de `frame_id` do RPLIDAR** em `launch/rbd_robo_hardware_launch.py` (o `sllidar_ros2` publica `/scan` com `frame_id="laser"` por padrão; o URDF real usa `laser_link` — sem o fix, o TF não bate e o Nav2 não monta o costmap a partir do laser). Aplicado junto com a troca para `sllidar_a1_launch.py` (launch por modelo, na versão atual do `sllidar_ros2`) e `serial_port:='/dev/rplidar'`.
8. ✅ **Terminal 1 (no robô)**: `rbd2_robo_hardware` — sobe driver Arduino + RPLIDAR; `/scan`, `/odom`, `/imu` e a TF confirmados consistentes (sem frames ausentes). **Rodas mecanum testadas com `rbd2_teclado` (teleop direto em `/cmd_vel`, sem precisar do `rbd2_bringup`) — motores respondendo corretamente (2026-07-30). IMU corrigida (bug de udev com CH340 duplicado, ver seção de depuração abaixo) e validada com dados reais (2026-07-31).**
9. ✅ **Terminal 2 (no robô ou no PC, mesma `ROS_DOMAIN_ID`)**: `rbd2_bringup_rviz` — Nav2 + RViz2 com o mapa provisório. Confirmado: AMCL, map_server e ambos os lifecycle managers ativos, `/map` publicado, RViz2 recebendo scan/TF/costmaps reais (fix do bug de composição do Nav2 na Pi — ver depuração abaixo).
10. ✅ **Definir a pose inicial** no RViz2 com "2D Pose Estimate" (no robô real `set_initial_pose: false` — sem isso o Nav2 não sabe onde o robô está). Confirmado manualmente na sessão de 2026-07-31: clique no RViz2 aceito pelo AMCL, TF `map→odom` passou a fluir.
11. 🎯 **Próximo passo — Terminal 3 (opcional)**: `rbd2_navega` — inicia a patrulha autónoma.

**Nota:** o programa de autostart do controle remoto (`rosmaster_main.py`) funciona normalmente com a placa expansora ligada, mas consome mais energia (mantém RPLIDAR e serial ativos) e ocupa `/dev/myserial` — por isso o passo 1 é sempre necessário antes de trabalhar com ROS2.

### 🐛 Depuração 2026-07-31 — IMU sem dados (accel/gyro/mag zerados)

Ao subir `rbd2_robo_hardware` limpo, `/odom` e `/scan` (com `frame_id: laser_link` correto) publicaram normalmente e a TF (`odom→base_footprint`, `base_link→laser_link`) ficou consistente — confirmando os passos 7 e 8 acima. Mas o `imu_filter_madgwick` ficou em warning constante (`The IMU seems to be in free fall`), e `/imu/data_raw` mostrou aceleração sempre `(0, 0, 0)`.

**Investigação:**
1. Comparado `Mcnamu_driver_X3.py` e `Rosmaster_Lib.py` entre o container original (`yahboomtechnology/ros-foxy:4.0.5`) e o `robodog2_humble` → **idênticos** (só diferem comentários pedagógicos). Pacotes ausentes no novo container (`yahboomcar_slam`, `yahboomcar_multi`, `yahboomcar_point`, `yahboomcar_KCFTracker`, `robot_pose_publisher_ros2`) não são usados no bringup — descartada diferença de compilação como causa.
2. Teste isolado com `Rosmaster_Lib` (fora do ROS2) mostrou `get_version()` retornando `-1` e bateria `0.0` — não é só o IMU, é a porta inteira sem resposta.
3. Teste com `pyserial` puro (sem `Rosmaster_Lib`), em escuta passiva por 4s: **0 bytes recebidos**. TX (Pi → Arduino) funciona; RX (Arduino → Pi) está mudo.
4. `dmesg` confirmou que após o power-cycle da placa expansora o CH340 (Arduino) reconectou corretamente como `ttyUSB2`, e `/dev/myserial` aponta pra ele certo — mapeamento de porta e udev **não são a causa**.

**Erro cometido durante a depuração (lição para não repetir):** rodei um script Python de diagnóstico (`Rosmaster()` standalone) **enquanto o `Mcnamu_driver_X3` do `rbd2_robo_hardware` já estava rodando e segurando `/dev/myserial`** — dois processos abrindo a mesma porta serial ao mesmo tempo, o mesmo tipo de conflito descrito na nota acima sobre `rosmaster_main.py`. Antes de qualquer teste standalone de serial, **sempre matar todos os processos do `rbd_robo_hardware_launch.py`** (o `ros2 launch` deixa processos filhos órfãos ao ser encerrado — `pkill -f rbd_robo_hardware` mata só o pai; pode ser necessário `kill -9` nos PIDs filhos individualmente, verificar com `ps aux | grep -E 'Mcnamu|sllidar|base_node|madgwick|ekf_node|joy_X3'`).

**Causa raiz encontrada (2026-07-31, sessão seguinte):** com tudo religado do zero e um único processo segurando `/dev/myserial`, o sintoma persistiu (`/voltage` em `0.0`, IMU zerada) — descartando de vez a hipótese de travamento de estado do power-cycle. Investigação do `dmesg` revelou **dois dispositivos CH340 idênticos** (`idVendor=1a86, idProduct=7523`) ligados na Pi ao mesmo tempo:

- `ttyUSB0` — porta USB `1-1.1`, ligada **direto** na Pi (fora do hub da placa expansora)
- `ttyUSB1` — porta USB `1-1.2.2`, **dentro do hub** da placa expansora (mesmo hub onde está o RPLIDAR em `1-1.2.1`)

A regra `udev` em `/etc/udev/rules.d/usb.rules` casava o symlink `myserial` só por `idVendor`/`idProduct`, sem distinguir a porta física — com dois dispositivos casando a mesma regra, o `/dev/myserial` podia resolver para qualquer um dos dois dependendo da ordem de enumeração USB no boot. Teste direto com `Rosmaster_Lib` confirmou qual é qual:

```python
Rosmaster(com='/dev/ttyUSB0')  # → version 3.3, battery 11.5V — Arduino real
Rosmaster(com='/dev/ttyUSB1')  # → sem resposta (o dispositivo do hub não fala o protocolo Rosmaster)
```

Ou seja: nesta sessão o `/dev/myserial` tinha resolvido para o CH340 errado (o do hub, não o Arduino) — explicando o comportamento intermitente entre sessões de depuração. Ainda não identificado fisicamente o que é o segundo dispositivo CH340 do hub (possível acessório da placa expansora não documentado).

**Fix aplicado:** regra `udev` pinada na porta física do Arduino confirmado (backup em `usb.rules.bak_20260731`):
```
KERNEL=="ttyUSB*", KERNELS=="1-1.1", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```
Após `udevadm control --reload-rules && udevadm trigger --subsystem-match=tty --action=add`, `/dev/myserial → ttyUSB0` (confirmado) e `/dev/rplidar → ttyUSB2` (inalterado).

**Validado após o fix:** `rbd2_robo_hardware` relançado — `/imu/data_raw` com aceleração real (`z ≈ 9.72 m/s²` parado, giro ≈ 0), sem warnings de "free fall"; `/voltage` em `11.4V`; TF `odom→base_footprint` consistente. Passos 7 e 8 confirmados de ponta a ponta.

**Risco conhecido do fix:** a regra pina pela porta física `1-1.1` — se o cabo do Arduino for movido para outra porta USB da Pi, a regra para de funcionar até ser atualizada manualmente.

**Próximo passo:** avançar para o passo 9 — `rbd2_bringup_rviz` (Nav2 + RViz2 com mapa provisório).

### 🐛 Depuração 2026-07-31 (continuação) — AMCL não subia com `rbd2_bringup_rviz`

Ao testar o passo 9 pela primeira vez (com a IMU já corrigida), o Nav2 subiu (map_server, controller_server, planner_server, bt_navigator, costmaps) mas o **AMCL nunca aparecia** em `ros2 node list` — sem nenhum erro visível no log. Sem AMCL não há transform `map→odom`, então o RViz nunca teria mapa localizável e o "2D Pose Estimate" não funcionaria.

**Causa raiz:** o `nav2_bringup` usa `use_composition: true` por padrão — todos os nós Nav2 sobem dentro de **um único processo** (`nav2_container`), carregados via chamadas de serviço ROS2 (`load_node`). Na Raspberry Pi 4B, sob carga de CPU, essa chamada de serviço para carregar o `map_server` sofreu **timeout** (`WARN: failed to send response to /nav2_container/_container/load_node (timeout)`) — o `map_server` chegou a subir internamente, mas o `launch_ros` nunca recebeu a confirmação e **abortou silenciosamente** o resto do grupo de localização (AMCL + `lifecycle_manager_localization` nunca foram sequer solicitados).

Confirmado isolando o teste: `ros2 launch nav2_bringup bringup_launch.py ... use_composition:=False` fez o AMCL subir normalmente, com seu próprio `lifecycle_manager_localization`, junto do `lifecycle_manager_navigation` da navegação.

**Fix aplicado** (`launch/navigation_dwa_launch.py` + `launch/rbd_bringup.launch.py`):
- `navigation_dwa_launch.py` ganhou o argumento `use_composition` (default `True`, preserva o comportamento em simulação no PC, onde nunca houve esse problema)
- `rbd_bringup.launch.py` (usado só no robô real) passa `use_composition:='False'` explicitamente — processos Nav2 separados em vez de compostos, evitando o timeout de carregamento na Pi

**⚠️ Correção importante:** a primeira "validação" do fix (feita logo em seguida, via `ros2 node list` mostrando `/amcl` + `/lifecycle_manager_localization` separados) foi um **falso positivo**. Motivo: o container `robodog2_humble` mantém seu **próprio clone git** de `robodog2` em `/home/rbd/ros2_ws/src/robodog2`, independente do clone no host onde o Claude Code estava editando os arquivos — o `colcon build` rodado logo após a edição recompilou o código **antigo** (sem o fix), e o AMCL só subiu "por sorte" porque a Pi estava com menos carga naquele instante específico, permitindo que a composição padrão (`use_composition: true`) completasse a tempo sem timeout. `ros2 node list` não distingue nós compostos de standalone — só checar processos do SO (`ps aux`) revela isso de verdade.

**Lição:** depois de commitar/pushar mudanças de código pelo Claude Code (rodando no host), é preciso `git pull` dentro do clone do container (`docker exec ... git -C /home/rbd/ros2_ws/src/robodog2 pull`) antes de `colcon build` — os dois clones **não** se sincronizam sozinhos.

**Validado de verdade** depois de sincronizar o container (`git pull` → `colcon build`) e relançar: `ps aux` dentro do container confirma **nenhum processo `component_container_isolated`/`nav2_container`** — `amcl`, `map_server`, `controller_server`, `planner_server`, `bt_navigator`, `behavior_server`, `smoother_server`, `waypoint_follower`, `velocity_smoother` e os dois `lifecycle_manager` todos como processos separados. Pose inicial publicada em `/initialpose` (x:-3.0, y:-2.0, yaw:0 — mesmo ponto de spawn da simulação `cma_vazio.world`) foi aceita pelo AMCL (`Setting pose (...): -3.000 -2.000 0.000`) e a TF `map→odom` passou a fluir.

**Nota — erro cosmético do RViz:** aparece um erro de shader (`GLSL link result: active samplers with a different type refer to the same texture image unit`, em `indexed_8bit_image.frag`) ao renderizar a textura do mapa — provavelmente driver de GPU da Pi (categoria semelhante ao fix `OGRE_RTT_MODE=Copy` já documentado para VMs). Não afeta a funcionalidade do Nav2.

**Nota — carga do sistema:** rodar hardware real + Nav2 descomposto (10 processos) + RViz2 juntos também pesa bastante na Pi 4B (load average chegou a 9–13 durante os testes) — comandos `ros2` de introspecção (`topic echo`, `tf2_echo`, `node list`) ficaram lentos ou falharam com `rcl node's context is invalid` sob essa carga. Não é um bug do Nav2/AMCL, é sintoma de sobrecarga — para diagnosticar de forma confiável, dar mais tempo entre comandos ou reduzir o que está rodando simultaneamente.

### 🐛 Achado 2026-07-31 (continuação) — sinais do RPLIDAR aparecem invertidos no RViz

Com o robô fisicamente sobre uma mesa (fora da base real, testes de bancada) e um livro colocado propositalmente na frente do sensor, o `/scan` no RViz mostrou o obstáculo (livro) **atrás** do robô em vez de na frente — os sinais do lidar estão invertidos 180°.

**Hipótese:** o `laser_joint` em `yahboomcar_description/urdf/yahboomcar_X3.urdf` define `rpy="0 0 0"` entre `base_link` e `laser_link` — ou seja, o URDF assume que o "ângulo zero" do RPLIDAR aponta para a frente do robô, sem nenhuma rotação de correção. Se a unidade física está montada com o conector/referência de ângulo zero voltado para trás, o resultado é exatamente essa inversão observada.

**Fix proposto (ainda não implementado):** como não é permitido editar arquivos-fonte de `yahboomcar_*` diretamente (ver `CLAUDE.md`), criar um pacote `robodog2_description` com uma cópia do URDF corrigida (`laser_joint` com `rpy="0 0 3.14159"`), e apontar `rbd_robo_hardware_launch.py` (que já é nosso, em `robodog2/launch/`) para usar essa versão em vez da original. Antes de implementar, vale confirmar fisicamente a marca de "frente" na carcaça do RPLIDAR A1, para garantir que a causa é mesmo montagem invertida e não outra coisa (ex: parâmetro do driver `sllidar_ros2`).

**Adiado para próxima sessão** — Pi estava sob carga alta ao final desta sessão.

### 🐛 Achado 2026-07-31 (continuação) — Gazebo não é viável na Raspberry Pi

Tentativa de rodar o teste de regressão da simulação (`rbd_simulador_x3_launch.py`, casa `cma_vazio`) **dentro do próprio container `robodog2_humble`** (que tem Gazebo Fortress 6.18 instalado) sobrecarregou a Pi 4B: `load average` chegou a **13.84**, e comandos simples como `ros2 topic list` levaram **~18 segundos** para responder. Também revelou processos órfãos acumulados de lançamentos anteriores da sessão (ver lição abaixo) que pioraram ainda mais a sobrecarga.

**Conclusão:** apesar de o `robodog2_humble` ter Gazebo Fortress + RViz2 instalados (documentado como possível no `CLAUDE.md`), rodar a simulação completa (física + Nav2 + RViz) na própria Pi não é praticável. **Testes de regressão da simulação devem ser feitos no PC de desenvolvimento** (Ubuntu 22.04 + Gazebo Fortress), não na Pi.

### 📝 Lição — limpeza de processos `ros2 launch` dentro do container

Matar só os processos filhos encontrados por `ps aux | grep <nome_do_nó>` não é suficiente — o processo pai `ros2 launch` pode continuar vivo e novos filhos (como `joint_state_publisher`/`robot_state_publisher`) escapam de greps focados em nomes de nós específicos. Processos órfãos de testes de horas atrás foram encontrados ainda rodando nesta sessão, contribuindo para a sobrecarga da Pi. Para limpar de verdade: `ps aux | grep -E '/opt/ros/humble/(lib|bin)|/home/rbd/ros2_ws/install'` (sem filtrar por nome de nó) e matar todos os PIDs retornados, incluindo o `ros2 launch` em si.

### ✅ Pose inicial confirmada manualmente (2026-07-31)

Com o AMCL validado de verdade (seção acima), a pose inicial foi testada da forma real de uso — clique em "2D Pose Estimate" no RViz2, sem publicar `/initialpose` via linha de comando. Aceita normalmente pelo AMCL, TF `map→odom` consistente. **Passo 10 do fluxo de hardware físico concluído.**

**Incidente durante a sessão:** logo após essa confirmação, com RViz2 + Nav2 descomposto + hardware ainda todos rodando (Pi já sob carga alta, ver nota acima), a sessão do Claude Code travou ao tentar registrar esse avanço no README. **Lição:** encerrar ou pelo menos minimizar RViz2/Nav2 antes de tarefas longas de edição/documentação enquanto a pilha real está no ar — a carga da Pi (load 9–13) afeta também o próprio Claude Code rodando no host, não só comandos `ros2`.

### 🐛 Reconfirmado 2026-07-31 — inversão do lidar real (frente/trás)

Novo teste do robô físico reconfirmou a inversão já registrada acima: `/scan` real aparece invertido 180° no RViz2 (sinal que deveria estar na frente aparece atrás). **Ainda não testado no simulador Gazebo** para confirmar se o mesmo comportamento aparece lá — teste anterior em simulação não indicou esse problema, o que reforça a hipótese de causa física (montagem do RPLIDAR) ou do URDF real (`yahboomcar_X3.urdf`), não do driver `sllidar_ros2` em si. Fix proposto continua o mesmo: pacote `robodog2_description` com `laser_joint` corrigido (`rpy="0 0 3.14159"`).

**Decisão:** antes de abrir o PR desta sessão, repetir os testes (pose inicial + observação do lidar) para confirmar que tudo está estável, já que a sessão anterior foi interrompida pelo travamento do Claude Code. PR fica para depois dessa nova rodada de testes.

**Próximo passo:** retestar pose inicial + inversão do lidar (incluindo no simulador Gazebo, no PC dev) antes de abrir o PR; depois resolver a inversão do lidar (`robodog2_description`) e rodar o teste de regressão da simulação no PC.

### Aliases `rbd2_*` dentro do `robodog2_humble`

O container já tem `/root/.bash_aliases` com todos os aliases da seção [Aliases](#aliases-bash_aliases) abaixo, incluindo o `source` automático do ambiente ROS2 (`/opt/ros/humble/setup.bash` + `install/setup.bash`). Como `docker exec` entra como `root` (`$HOME=/root`) mas o workspace vive em `/home/rbd/ros2_ws`, os aliases usam `$RBD2_WS` explicitamente em vez de `~/ros2_ws`. **Terminais abertos antes dessa configuração precisam rodar `source ~/.bash_aliases` manualmente uma vez** para carregar o ambiente.

### Manutenção — espaço em disco do container

Cada `docker commit` do `robodog2_humble` gera uma imagem de ~4.6GB. Snapshots antigos acumulam rápido e podem lotar o disco da Pi (já aconteceu em 2026-07-30 — partição raiz foi a 0 disponível). Boas práticas:
- Manter só o snapshot mais recente confirmado bom (`docker images robodog2_humble_snapshot` + `docker rmi` dos antigos).
- **Sempre pedir confirmação antes de rodar `docker commit`** — a operação pausa o container (todos os processos congelam) e demora, então evitar rodar no meio de um teste com motores em movimento.
- `docker system df` mostra rapidamente quanto espaço é reciclável.

---

## Ambiente de desenvolvimento

- Ubuntu 22.04, ROS2 Humble
- Gazebo Fortress v6.17.1 (`ign gazebo`) — **NÃO é Gazebo Harmonic**
- Workspace principal: `~/ros2_ws/`

---

## Status atual (2026-07-30)

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
- **`robodog2_humble` operacional no ROSMASTER X3 físico**: `rbd2_robo_hardware` sobe driver Arduino + RPLIDAR sem erro, `/scan`/`/odom`/`/imu`/TF consistentes, fix de `frame_id` do RPLIDAR aplicado
- **IMU real validada (2026-07-31)** — bug de udev corrigido (CH340 duplicado causava symlink `/dev/myserial` ambíguo); `/imu/data_raw` com aceleração e giro reais, sem warnings de "free fall"
- **Nav2 real com AMCL validado (2026-07-31)** — bug de composição do `nav2_bringup` corrigido (`use_composition:=False` no robô real evita timeout de carregamento do AMCL na Pi 4B); `rbd2_bringup_rviz` sobe com AMCL, map_server e RViz2 recebendo sinais reais
- **Rodas mecanum reais testadas** via `rbd2_teclado` (teleop direto em `/cmd_vel`) — motores respondendo corretamente (2026-07-30)
- **Aliases `rbd2_*` ativos dentro do `robodog2_humble`** — ver seção "Containers Docker no ROSMASTER X3 físico"
- **Pose inicial real confirmada (2026-07-31)** — "2D Pose Estimate" no RViz2 aceito pelo AMCL, TF `map→odom` consistente (passo 10 do fluxo de hardware concluído)

### Em progresso 🎯

- **Lava tube v1.1** — validar em Gazebo teleop + lidar na zona navegável parcial (`rbd_lava_tube`)
- Testar código Yahboom original no Gazebo — comparar comportamento de navegação com robodog2
- **Inversão do lidar real (frente/trás)** — reconfirmada em 2026-07-31; ainda falta testar no simulador Gazebo para confirmar se o comportamento se repete lá
- **Próximo passo imediato:** retestar pose inicial + inversão do lidar (incluindo no simulador, no PC dev) antes de abrir o PR desta sessão — sessão anterior foi interrompida por travamento do Claude Code sob carga alta da Pi

### Por fazer ❌

- Testar código Yahboom no robot real (X3 físico)
- Integrar Rosmaster ↔ robodog2 — cruzar o melhor dos dois códigos
- SLAM real da casa física → gerar mapa físico (ver "Estratégia de pose inicial" no `CLAUDE.md`)
- Calibração de `rbd_tabelas.py` para a casa real (waypoints do robô físico)
- Ciclo autónomo completo (`rbd2_navega`) em hardware físico
- Corrigir inversão do lidar real (pacote `robodog2_description` com `laser_joint` ajustado)
- Testar `rbd2_navega` no robô físico com o mapa provisório

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

# Robô real — camada de hardware (correr NO robô, dentro do container)
alias rbd2_robo_hardware='ros2 launch robodog2 rbd_robo_hardware_launch.py'

# Robô real — Nav2 + RViz (pode correr no PC remoto via rede ROS2)
alias rbd2_bringup='ros2 launch robodog2 rbd_bringup.launch.py map:=$(ros2 pkg prefix robodog2)/share/robodog2/maps/rbd_mapa_vazio.yaml'
alias rbd2_bringup_rviz='ros2 launch robodog2 rbd_bringup.launch.py rviz:=true map:=$(ros2 pkg prefix robodog2)/share/robodog2/maps/rbd_mapa_vazio.yaml'
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

### Robô real — hardware real, sem Gazebo
```bash
# Pré-requisito: robodog2 compilado e instalado no container do X3
#   colcon build --packages-select robodog2 && source install/setup.bash

# Terminal 1 — NO ROBÔ (container ROS2)
rbd2_robo_hardware          # drivers Yahboom + RPLIDAR A1 (publica /scan, /odom, TF)

# Terminal 2 — NO PC ou NO ROBÔ (rede ROS2 com mesmo ROS_DOMAIN_ID)
rbd2_bringup                # Nav2 (AMCL + DWB) com mapa da casa vazia
# ou com RViz2 visível no PC:
rbd2_bringup_rviz

# Após lançar: usar "2D Pose Estimate" no RViz2 para definir a pose inicial no mapa

# Terminal 3 — patrulha autónoma (opcional)
rbd2_navega
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

**Arquitetura do robô real (sem Gazebo):**
```
rbd_robo_hardware_launch.py           ← corre NO ROBÔ (container)
├── yahboomcar_bringup_X3_launch.py   ← driver Arduino (Mcnamu_driver_X3)
│   ├── Mcnamu_driver_X3              → publica /imu/data_raw, /vel_raw, /joint_states
│   ├── base_node_X3                  → calcula /odom a partir de /vel_raw
│   ├── imu_filter_madgwick           → fusão IMU → /imu/data
│   ├── ekf (robot_localization)      → /odom melhorado + TF odom→base_footprint
│   └── robot_state_publisher         ← URDF: yahboomcar_X3.urdf
└── sllidar_launch.py (sllidar_ros2)  → publica /scan (RPLIDAR A1, /dev/ttyUSB0)

rbd_bringup.launch.py                 ← pode correr no PC via rede ROS2
├── navigation_dwa_launch.py          ← Nav2: AMCL + DWB + BT Navigator + recoveries
│                                        use_sim_time=false
│                                        params: params/rbd_dwa_nav_params_real.yaml
├── rviz2 (opcional, rviz:=true)      ← config: rviz/robodog2.rviz
└── rbd_navega (opcional, navega:=true) ← patrulha autónoma por pesos
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
| `worlds/lava_tube.world` | Lava tube lunar (1/6g), v1.1 — entrada semi-enterrada, rampa, zona navegável parcial; gerado por `generate_lava_tube.py` | 🎯 validar (`lava_tubes_grok`) |
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
