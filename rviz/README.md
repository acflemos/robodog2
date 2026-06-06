# rviz/ — Configurações do RViz2

## Arquivos

| Arquivo | Descrição |
|---|---|
| [robodog2.rviz](robodog2.rviz) | Configuração principal RViz2 (ROS2). Usada por `rbd2_simulador_x3`. |
| [robodog1.rviz](robodog1.rviz) | Configuração original ROS1 — mantida como referência histórica. Não compatível com RViz2. |

---

## robodog2.rviz — displays activos

| Display | Tópico | Notas |
|---|---|---|
| Grid | — | Células de 1m, plano XY |
| LaserScan | `/scan` | Verde, 360°, Flat Squares |
| RobotModel | `/robot_description` | Links do X3 |
| TF | — | Cadeia `map → odom → base_footprint → base_link` |
| Map (global_costmap) | `/global_costmap/costmap` | Mapa de custo global |
| Map | `/map` | Mapa de navegação (AMCL/map_server) |
| Path (global_path) | `/plan` | Plano global Nav2 (verde) |
| PoseArray | `/particle_cloud` | Nuvem de partículas AMCL |
| Map (local_costmap) | `/local_costmap/costmap` | Mapa de custo local |
| Odometry | `/odom` | Odometria com elipse de covariância |
| Path (local_path) | `/local_plan` | Plano local DWB (ciano) |
| PoseWithCovariance | `/amcl_pose` | Pose estimada pelo AMCL |
| Pose (goal) | `/goal_pose` | Destino de navegação |

- **Fixed Frame:** `map`
- **Vista inicial:** centrada em (-3.0, -2.0) — posição de spawn do X3
- **Painel Nav2:** botões Nav2 para envio de goals e gestão da missão

---

## Diferenças em relação ao robodog1.rviz (ROS1 → ROS2)

| Aspecto | robodog1 (ROS1) | robodog2 (ROS2) |
|---|---|---|
| Classes display | `rviz/Grid`, `rviz/LaserScan` | `rviz_default_plugins/Grid`, etc. |
| Partículas AMCL | `/particlecloud` | `/particle_cloud` |
| Plano global | `/move_base/NavfnROS/plan` | `/plan` |
| Plano local | `/move_base/TrajectoryPlannerROS/local_plan` | `/local_plan` |
| Costmap global | `/move_base/global_costmap/costmap` | `/global_costmap/costmap` |
| Costmap local | `/move_base/local_costmap/costmap` | `/local_costmap/costmap` |
| Painel navegação | Interactive Markers ROS1 | `nav2_rviz_plugins/Navigation 2` |
