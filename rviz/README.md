# rviz/ — Configurações do RViz

Esta pasta contém os arquivos de configuração do RViz originados no projeto **robodog1 (ROS1)**.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| [robodog1.rviz](robodog1.rviz) | Configuração completa do RViz 2 para visualização e navegação do robodog. |

---

## O que o robodog1.rviz exibe

| Display | Tópico/Fonte | Notas |
|---|---|---|
| Grid | — | Células de 1m, plano XY |
| RobotModel | `/robot_description` | Colisões desativadas |
| TF | — | Árvore completa: `map → odom → base_footprint → base_link` |
| LaserScan | `/scan` | Verde, 360°, estilo flat squares |
| Map | `/map` | Mapa de custo global (AMCL) |
| Path | `/move_base/NavfnROS/plan` | Plano global de navegação |
| Path | `/move_base/TrajectoryPlannerROS/local_plan` | Plano local (DWA) |
| Costmap | `/move_base/global_costmap/costmap` | Mapa de custo global |
| Costmap | `/move_base/local_costmap/costmap` | Mapa de custo local |
| PoseArray | `/particlecloud` | Nuvem de partículas AMCL |
| Range | `/ultrasonico_f` | Ultrassónico frente |
| Range | `/ultrasonico_t` | Ultrassónico trás |
| Range | `/ultrasonico_d` | Ultrassónico direita |
| Range | `/ultrasonico_e` | Ultrassónico esquerda |
| InteractiveMarkers | `/move_base_simple/goal` | Destino de navegação |

- **Fixed Frame:** `map`  
- **Taxa de atualização:** 30 FPS

---

## Adaptação para ROS2 (próximos passos)

- [ ] O arquivo `.rviz` é compatível com RViz2 (formato YAML idêntico), mas os tópicos do `move_base` (ROS1) precisam ser substituídos pelos equivalentes do **Nav2** (ROS2):
  - `/move_base/NavfnROS/plan` → `/plan`
  - `/move_base/TrajectoryPlannerROS/local_plan` → `/local_plan`
  - `/move_base/global_costmap/costmap` → `/global_costmap/costmap`
  - `/move_base/local_costmap/costmap` → `/local_costmap/costmap`
  - `/particlecloud` → `/particle_cloud`
- [ ] Criar uma cópia `robodog2.rviz` com os tópicos atualizados para Nav2
- [ ] Verificar compatibilidade do display `Range` com RViz2 (plugin `rviz_default_plugins`)
