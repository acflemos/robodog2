# Lava tubes no curso de ROS2 — por que este cenário?

Este documento explica a **proposta pedagógica** do ambiente simulado de lava tube lunar no projeto robodog2. Para detalhes técnicos de implementação, ver [PLANEJAMENTO_LAVA_TUBE.md](PLANEJAMENTO_LAVA_TUBE.md).

---

## Dois mundos, uma mesma stack

O curso de ROS2 que estamos a construir oferece **dois ambientes complementares**:

| Ambiente | Onde corre | Papel no curso |
|----------|------------|----------------|
| **Casa simulada** (`cma_moveis`) | Gazebo + robô real | Aprender SLAM, Nav2 e navegação autónoma num cenário familiar — o que o aluno pode replicar em casa |
| **Lava tube lunar** (`lava_tube`) | Gazebo (gravidade 1/6g) | O mesmo conhecimento ROS2 aplicado a um cenário de **exploração espacial** — o que desperta ambição e sentido |

O ambiente doméstico responde à pergunta: *“Isto funciona no mundo real?”*  
O lava tube responde à pergunta: *“Para que serve robótica além da sala de estar?”*

Não são concursos separados. O aluno usa os **mesmos conceitos** — tópicos, nós, mapas, planeamento de trajetórias — mas o segundo cenário coloca-o numa narrativa onde a robótica é **infraestrutura civilizacional**, não apenas conveniência.

---

## Por que lava tubes?

**Lava tubes** são túneis naturais formados por rios de lava solidificada. Existem na Terra, na Lua e em Marte. Na exploração espacial, são candidatos privilegiados a habitats humanos porque:

1. **Proteção contra radiação** — a rocha acima do túnel funciona como escudo natural; na superfície lunar ou marciana, a radiação cósmica e solar é um risco permanente para colonos.
2. **Temperatura mais estável** — o subsolo atenua os extremos térmicos da superfície.
3. **Escala adequada** — tubos lunares identificados por orbitadores podem ter dezenas ou centenas de metros de largura — espaço suficiente para instalações, estradas internas e eventualmente **cidades protegidas**.
4. **Acesso robótico primeiro** — antes de humanos entrarem, é preciso mapear, inspecionar estruturalmente e preparar o interior. Isso é trabalho para **robôs autónomos** com sensores, SLAM e navegação — exactamente o que o curso ensina.

A missão simulada do robodog no lava tube não é ficção distante: espelha problemas reais que agências espaciais e empresas privadas já estudam para presença humana sustentada na Lua e em Marte.

---

## O que o aluno vive na simulação

1. **Entrada no túnel** — gravidade lunar, escuridão, necessidade de mapear o desconhecido.
2. **Exploração** — teleoperação, SLAM, construção de mapa ao longo de um corredor em curva com alcova lateral.
3. **Recompensa narrativa** — na **zona do Enigma**, no final do túnel: restos de uma missão antiga, beacon ainda emissivo, símbolos que convidam a perguntar *quem esteve aqui antes*.

A progressão técnica do curso pode evoluir em paralelo:

- **Fase 1** — robô com rodas no túnel (acessível, pedagógico).
- **Fase 2** — robô híbrido pernas + rodas no **mesmo** mundo (mobilidade para terreno irregular).
- **Decoração visual** — interior rochoso credível (referência validada com meshes DARPA SubT), mantendo piso plano para navegação.

O aluno percebe que ROS2 não é só para aspiradores: é a camada de software que pode unir sensores, decisão e acção em ambientes onde nenhum humano ainda pisou.

---

## Robôs que constroem o futuro

As primeiras cidades humanas na Lua e em Marte — protegidas da radiação, abastadas de recursos locais, expandidas ao longo de décadas — **não serão erguidas apenas por astronautas com ferramentas**. Serão precedidas e acompanhadas por frotas de robôs que:

- mapeiam lava tubes e escolhem locais seguros;
- removem detritos e preparam o piso;
- instalam estruturas infláveis ou modulares sob a rocha;
- mantêm túneis, sensores e comunicações sem exposição humana contínua.

Muitos desses sistemas precisarão de **inteligência embarcada**, fusão de sensores, planeamento robusto e operação autónoma ou teleoperada — competências centrais de um curso sério de ROS2.

O robodog no lava tube é um **primeiro passo em miniatura** dessa visão: pequeno no simulador, grande no significado para quem está a aprender.

---

## Como experimentar

```bash
rbd2_build_pkg && rbd2_source
source ~/.bash_aliases

rbd_lava_tube        # túnel operacional (navegação com rodas)
rbd_lava_tube_fuel   # referência visual do interior rochoso
```

Para a casa simulada e o robô real, o fluxo habitual do projeto (`rbd2_simulador_x3_moveis`, `rbd2_navega`, etc.) permanece inalterado.

---

## Documentos relacionados

- [PLANEJAMENTO_LAVA_TUBE.md](PLANEJAMENTO_LAVA_TUBE.md) — fases técnicas, artefatos do Enigma, decisões de geometria
- [worlds/README.md](../worlds/README.md) — ficheiros `.world` e aliases de lançamento
- [README.md](../README.md) — visão geral do pacote robodog2

---

*Projeto robodog2 — robótica doméstica que aponta para a exploração espacial.*