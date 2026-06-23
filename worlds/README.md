# worlds/

Mundos Gazebo Fortress para simulação do robodog2.

## Arquivos

| Arquivo | Descrição | Usado por |
|---|---|---|
| [cma_vazio.world](cma_vazio.world) | Casa simulada sem móveis — 15 cômodos. Referência geométrica para calibração dos pontos de destino em `rbd_tabelas.py`. Mapa: `~/rbd_mapa_vazio.yaml`. | `rbd2_simulador_x3`, `rbd2_slam_x3_vazio` |
| [cma_moveis.world](cma_moveis.world) | Casa simulada com móveis — 79 modelos. Mundo de operação real do robô. | `rbd2_simulador_x3_moveis`, `rbd2_slam_x3_moveis` |
| [rbd_gz_empty.world](rbd_gz_empty.world) | Mundo vazio para testes rápidos de spawn e teleop. | `rbd2_gz_x3` (default) |
| [lava_tube.world](lava_tube.world) | Lava tube lunar (1/6g), túnel em caixa oca (v1 aprovada), câmara final com enigma. Gerado por [generate_lava_tube.py](generate_lava_tube.py). | `rbd_lava_tube` |
| [lava_tube_fuel.world](lava_tube_fuel.world) | Protótipo com meshes Fuel (Cave Straight 02 Type B + Cap). Descarrega da internet na 1ª execução. | `rbd_lava_tube_fuel` ou `ros2 launch robodog2 rbd_lava_tube_fuel_launch.py` |

Após `git pull`, execute `rbd2_build_pkg && rbd2_source` antes de lançar mundos novos.

## Notas de compatibilidade

Os mundos foram convertidos de Gazebo Classic (SDF 1.6) para Gazebo Fortress:
- Poses dos modelos atualizadas a partir do bloco `<state>` do arquivo original
- Plugin de física substituído pelo padrão Fortress
- Todos os modelos validados sem erros de spawn no Ignition Gazebo v6.17.1
