# worlds/ — Ambientes de Simulação Gazebo

Esta pasta contém os arquivos de mundo (`.world`) para simulação no Gazebo, originados no projeto **robodog1 (ROS1)**. Todos estão no formato **SDF v1.4** com motor de física ODE.

---

## Arquivo de mundo mínimo

| Arquivo | Descrição |
|---|---|
| [empty.world](empty.world) | Mundo vazio com sol e plano de chão. Base para criar novos cenários. Physics ODE a 1000 Hz. |

---

## Ambientes de escritório / CMA (ambiente real mapeado)

Estes mundos representam o ambiente real do escritório que foi mapeado com o robodog1.

| Arquivo | Descrição |
|---|---|
| [escritorio_ma.world](escritorio_ma.world) | Ambiente de escritório principal (MA). Usado nos testes de navegação do robodog1. |
| [cma_*.world](.) | Variantes do ambiente CMA com diferentes configurações de móveis e obstáculos. |
| [cma_moveis_*.world](.) | Variantes com obstáculos dinâmicos/móveis para testes de replanejamento. |
| [Escritorio_MA/](Escritorio_MA/) | Subpasta com `model.config` e `model.sdf` do modelo do escritório para o Gazebo Model Database. |

---

## Ambientes TurtleBot3 (públicos)

Estes mundos são distribuídos com o pacote `turtlebot3_gazebo` e usados para testes padronizados.

| Arquivo | Descrição |
|---|---|
| [turtlebot3_stage_1.world](turtlebot3_stage_1.world) | Corredor simples com paredes — bom para testar navegação básica. |
| [turtlebot3_stage_2.world](turtlebot3_stage_2.world) | Ambiente com obstáculos variados. |
| [turtlebot3_stage_3.world](turtlebot3_stage_3.world) | Ambiente com câmaras (rooms). |
| [turtlebot3_stage_4.world](turtlebot3_stage_4.world) | Ambiente complexo com múltiplas salas. |
| [turtlebot3_house.world](turtlebot3_house.world) | Planta de casa residencial — bom para testes de mapeamento SLAM. |
| [turtlebot3_autorace.world](turtlebot3_autorace.world) | Pista de corrida autónoma com sinalização — referência para navegação estruturada. |

---

## Configuração física comum (todos os mundos)

```xml
<physics type="ode">
  <real_time_update_rate>1000.0</real_time_update_rate>
  <max_step_size>0.001</max_step_size>
</physics>
```

A taxa de 1000 Hz é alta para garantir estabilidade na simulação das rodas mecanum do X3.

---

## Compatibilidade com ROS2 (próximos passos)

Os arquivos `.world` SDF são **diretamente compatíveis com ROS2** — o Gazebo Classic (gazebo11) e o Ignition Gazebo lêem o mesmo formato SDF.

- [ ] Verificar se os plugins dos mundos (luzes, modelos) são compatíveis com `gazebo_ros` ROS2
- [ ] Criar launch file ROS2 (`spawn_world.launch.py`) que carregue estes mundos via `gazebo_ros` ou `ros_gz_sim`
- [ ] Para uso com **Ignition/Gazebo Harmonic**, converter os modelos SDF v1.4 para SDF v1.8+
- [ ] O ambiente `Escritorio_MA` pode ser reutilizado diretamente nos testes do robodog2
