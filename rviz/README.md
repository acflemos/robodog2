# rviz/

Configurações do RViz2 para o robodog2.

## Arquivos

| Arquivo | Usado por | Descrição |
|---|---|---|
| [robodog2.rviz](robodog2.rviz) | `rbd2_simulador_x3` | Visualização completa de navegação: Nav2 panel, mapa, costmaps local/global, paths global e local, partículas AMCL, laser scan, TF. |
| [map.rviz](map.rviz) | `rbd2_slam_x3_vazio` / `rbd2_slam_x3_moveis` | Visualização de mapeamento SLAM: mapa em construção, laser scan, TF. |

## Tópicos exibidos em robodog2.rviz

| Display | Tópico |
|---|---|
| Map | `/map` |
| Global Costmap | `/global_costmap/costmap` |
| Local Costmap | `/local_costmap/costmap` |
| Global Path | `/plan` |
| Local Path | `/local_plan` |
| Particle Cloud | `/particle_cloud` |
| LaserScan | `/scan` |
| RobotModel | `/robot_description` |
| TF | `map → odom → base_footprint` |
