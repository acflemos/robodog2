# worlds/

Mundos Gazebo Fortress para simulação do robodog2.

> **Lava tube no curso de ROS2:** por que este cenário existe — [docs/LAVA_TUBE.md](../docs/LAVA_TUBE.md)

## Arquivos

| Arquivo | Descrição | Usado por |
|---|---|---|
| [cma_vazio.world](cma_vazio.world) | Casa simulada sem móveis — 15 cômodos. Referência geométrica para calibração dos pontos de destino em `rbd_tabelas.py`. Mapa: `~/rbd_mapa_vazio.yaml`. | `rbd2_simulador_x3`, `rbd2_slam_x3_vazio` |
| [cma_moveis.world](cma_moveis.world) | Casa simulada com móveis — 79 modelos. Mundo de operação real do robô. | `rbd2_simulador_x3_moveis`, `rbd2_slam_x3_moveis` |
| [rbd_gz_empty.world](rbd_gz_empty.world) | Mundo vazio para testes rápidos de spawn e teleop. | `rbd2_gz_x3` (default) |
| [lava_tube.world](lava_tube.world) | Lava tube lunar (1/6g), v1.1 — entrada semi-enterrada, rampa, subida progressiva, zona navegável parcial (X3). Gerado por [generate_lava_tube.py](generate_lava_tube.py). | `rbd_lava_tube` |
| [lava_tube_fuel.world](lava_tube_fuel.world) | Referência visual Fuel — interior rochoso credível (validado). Piso irregular: **não** usar para colisão/navegação com rodas. Uso futuro: paredes/teto decorativos dentro do `lava_tube.world`. | `rbd_lava_tube_fuel` |

## Lava tube — como lançar (validado)

```bash
rbd2_build_pkg && rbd2_source
source ~/.bash_aliases

rbd_lava_tube        # túnel operacional (v1.1, zona navegável parcial com rodas)
rbd_lava_tube_fuel   # referência visual (meshes Fuel, internet na 1ª execução)
```

Aliases definidos em `~/.bash_aliases`. Requer `source ~/.bash_aliases` em terminais já abertos.

## Notas de compatibilidade

Os mundos foram convertidos de Gazebo Classic (SDF 1.6) para Gazebo Fortress:
- Poses dos modelos atualizadas a partir do bloco `<state>` do arquivo original
- Plugin de física substituído pelo padrão Fortress
- Todos os modelos validados sem erros de spawn no Ignition Gazebo v6.17.1
