# Planejamento — Lava Tube Lunar (robodog2)

> Documento de objetivos técnicos para a branch `lava_tubes_grok`.
> Para a **justificativa pedagógica** do cenário no curso de ROS2, ver [LAVA_TUBE.md](LAVA_TUBE.md).

## Visão geral

Criar um ambiente de simulação inspirador para um **curso de robótica com ROS2**, usando exploração de **lava tubes lunares** como cenário narrativo e técnico.

---

## Decisão v1.1 — Zona navegável parcial (robodog2)

> **Aprovada em 2026-06-26** na branch `lava_tubes_grok`.

O robodog2 (ROSmaster X3, rodas) **não precisa percorrer o lava tube inteiro**. Basta uma **porção inicial navegável** para o aluno experimentar o cenário lunar, ver o retorno do lidar e iniciar os primeiros mapas. O restante do túnel fica como **promessa de missão** — visível ao longe, inacessível com o hardware atual.

### Estratégia geométrica (implementada em v1.1)

1. **Entrada semi-enterrada** — abaixar o túnel na simulação de forma que ~metade da seção da boca fique acima do piso plano virtual (`lunar_surface` em `z=0`), como um lava tube real emergindo do regolito.
2. **Acesso por rampa** — ligar o piso externo ao piso interno nos primeiros metros, para o X3 entrar sem degrau na boca.
3. **Subida progressiva** — ao longo dos segmentos, o piso interno sobe gradualmente em relação ao nível externo; o robô avança, tenta subir e **fica preso** num limite natural para rodas (comportamento esperado, não falha).
4. **Vislumbre do Enigma** — antes do bloqueio físico, sensores e câmera captam ao longe a câmara final e artefatos (`ancient_beacon`, silhuetas do lander, etc.), despertando curiosidade.
5. **Continuação no robodog3** — exploração completa do túnel (curva S, alcova, câmara) fica para o **robodog3** (futuro: possivelmente **4 pernas** com **rodas na ponta das pernas**).

### Critérios de sucesso (Fase 1)

- Aluno entra no túnel, teleopera e mapeia a **zona acessível** com stack ROS2 existente (SLAM, Nav2, teleop).
- Lidar e mapa mostram o corredor escuro e, no limite, indícios da zona do Enigma.
- A limitação das rodas motiva explicitamente o estudo do robodog3 — mesma missão, nova arquitetura de mobilidade.

### Implementação v1.1

- `worlds/generate_lava_tube.py`: `TUBE_BURY=1.5 m`, rampa `entrance_ramp`, berms `entrance_berms`, `SEG_FLOOR_Z` progressivo, `wheel_barrier` em x≈27, spawn em (-6, 0, 0.1).
- `worlds/lava_tube.world` regenerado; validar com `rbd_lava_tube` (teleop + lidar na zona acessível).

---

## Fase 1 — Ambiente + robodog lunar (atual)

### Mundo
- **Lava tube realista** em Gazebo Fortress (`worlds/lava_tube.world`) — **v1 aprovada** (geometria base); **v1.1** aplica a decisão de zona navegável parcial acima
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
- **ROSmaster X3** (robodog2 atual) — rodas, hardware acessível, uso em casa
- Primeiro protagonista do cenário — explora apenas a **zona navegável parcial** do lava tube
- Stack ROS2 existente (SLAM, Nav2, teleop) aplicado ao cenário lunar

### Propósito pedagógico
- Demonstrar que robótica com ROS2 pode ser **interessante e motivadora** com hardware real e acessível
- Iniciar mapeamento e exploração num ambiente inspirador, sem exigir locomoção que o X3 não tem
- **Gancho narrativo:** vislumbre do Enigma + limite físico das rodas → motivação para o robodog3

---

## Fase 2 — robodog3 (posterior)

### Robô
- **robodog3** (a desenvolver) — arquitetura híbrida, possivelmente **4 pernas** com **rodas na ponta das pernas**
- Projetado para terreno irregular, degraus e subida no interior do lava tube
- Explora o **mesmo mundo** da Fase 1 até a câmara final e a zona do Enigma

### Propósito pedagógico
- **Continuação da missão** iniciada no robodog2 — não um cenário separado
- Contraste didático: mesma missão, **duas abordagens de mobilidade** (rodas vs. pernas+rodas)
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

Na **Fase 1 (robodog2)**, a recompensa é um **vislumbre ao longe** — o aluno vê o beacon e silhuetas antes do limite das rodas. Na **Fase 2 (robodog3)**, a recompensa é a **chegada física** à câmara e inspeção dos artefatos.

---

## Notas

- Branch de trabalho: `lava_tubes_grok`
- Simulador: Gazebo Fortress (Ignition Gazebo v6) — não Harmonic
- Documentação do curso: em organização paralela (Gemini)
- Lançar (aliases validados): `rbd_lava_tube` (operacional) e `rbd_lava_tube_fuel` (visual Fuel)
- Pré-requisito: `rbd2_build_pkg && rbd2_source && source ~/.bash_aliases`