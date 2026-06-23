# Planejamento — Lava Tube Lunar (robodog2)

> Documento de objetivos acordados para a branch `lava_tubes_grok`.
> A documentação pedagógica do curso está sendo organizada em paralelo (Gemini).

## Visão geral

Criar um ambiente de simulação inspirador para um **curso de robótica com ROS2**, usando exploração de **lava tubes lunares** como cenário narrativo e técnico.

---

## Fase 1 — Ambiente + robodog lunar (atual)

### Mundo
- **Lava tube realista** em Gazebo Fortress (`worlds/lava_tube.world`) — **v1 aprovada**
- **Gravidade lunar** (~1,62 m/s², ~1/6 da Terra)
- Geometria primitiva estática — otimizada para VM 12 núcleos / 16 GB RAM
- **Túnel em caixa oca** — piso + paredes + teto com espessura visível (colisão confiável)
- **Sem estalactites** — formação vulcânica seca (Lua sem água no passado)
- Túnel em curva S (~48 m) + alcova lateral + câmara final ampliada com skylight
- Regenerável via `python3 worlds/generate_lava_tube.py`
- **Decoração futura (Fase 1b):** meshes Fuel `Cave Straight 02 Type B` como **interior visual** dentro da caixa oca. Referência validada: `lava_tube_fuel.world` — zoom interno mostra túnel rochoso credível de lava tube
- **Piso Fuel descartado para colisão:** irregular demais para robô com rodas; piso plano da v1 mantém navegação; mesh Fuel só em paredes/teto (visual-only)
- **Zona do Enigma** (final do túnel): restos de uma antiga missão não-humana — lander corroído, antena tombada, painéis deteriorados, placa monolítica, **pirâmide pequena** e **beacon emissivo** ainda pulsando após eras (sugere que alguém esteve aqui há muito tempo)

### Robô
- Versão **maior** do robodog, com **aparência de veículo lunar**
- Primeiro protagonista do cenário — acessível pedagogicamente, serve de **inspiração** para estudantes
- Explora o lava tube com stack ROS2 existente (SLAM, Nav2, teleop)

### Propósito pedagógico
- Demonstrar que robótica com ROS2 pode ser **interessante e motivadora**
- Servir de **referência visual e narrativa** para o material do curso

---

## Fase 2 — Robodog híbrido pernas + rodas (posterior)

### Robô
- Novo robodog com **pernas e rodas** — arquitetura mais adequada ao terreno irregular do lava tube
- Explora o **mesmo mundo** da Fase 1, com **mais elegância** na locomoção

### Propósito pedagógico
- Contraste didático: mesma missão, **duas abordagens de mobilidade**
- Motivar estudantes a pensar em **arquitetura de robô** além de software

---

## Objetivo transversal

Tornar a robótica **muito interessante** para estudantes que queiram aprender **ROS2**, usando um cenário lunar credível e evolutivo (Fase 1 → Fase 2).

---

## Narrativa — Zona do Enigma

No final do lava tube, o robô descobre uma **câmara ampliada** iluminada por um fraco skylight. Os artefatos sugerem uma **missão antiga de origem desconhecida**:

| Elemento | Função narrativa |
|---|---|
| `ancient_lander` | Corpo achatado corroído — não se parece com engenharia humana recente |
| `ancient_dish` | Antena de comunicação tombada — missão interrompida há eras |
| `solar_debris` | Painéis deteriorados espalhados |
| `ancient_beacon` | Esfera emissiva ciano — **única luz ainda activa**, o mistério central |
| `ancient_plaque` | Monólito fino com brilho residual — "inscrição" sugerida |
| `mystery_pyramid` | Pirâmide em degraus — símbolo que desperta curiosidade |

Objetivo pedagógico: o estudante mapeia o túnel escuro e é **recompensado pela exploração** com uma revelação que motiva perguntas (Quem esteve aqui? Por quê? O beacon ainda funciona?).

---

## Notas

- Branch de trabalho: `lava_tubes_grok`
- Simulador: Gazebo Fortress (Ignition Gazebo v6) — não Harmonic
- Documentação do curso: em organização paralela (Gemini)
- Lançar (aliases validados): `rbd_lava_tube` (operacional) e `rbd_lava_tube_fuel` (visual Fuel)
- Pré-requisito: `rbd2_build_pkg && rbd2_source && source ~/.bash_aliases`