#!/usr/bin/env python3
"""Gera worlds/lava_tube.world — lava tube lunar, perfil meio-cilindro suave.

Estratégia visual (evita efeito 'escada espiral' de muitas caixas rotacionadas):
  - Colisão: túnel em caixa (piso plano + paredes) — parece e funciona como túnel
  - Visual da abóbada: um cilindro horizontal por segmento (superfície curva contínua)
  - Decoração: poucas rochas vulcânicas discretas (sem estalactites — Lua sem água)
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "lava_tube.world"

W, H, T = 4.0, 3.0, 0.2       # largura, altura interior, espessura parede
R = W / 2                      # raio do meio-cilindro visual
SEG_LEN = 8.0
FLOOR_THICK = 0.15

SEGMENTS = [
    (4.0, 0.0, 0.0),
    (12.0, 0.0, 0.0),
    (20.0, 0.4, 0.08),
    (28.0, 1.2, 0.16),
    (36.0, 2.0, 0.12),
    (44.0, 2.6, 0.05),
]

ROCK_SHADES = [
    ("0.16 0.13 0.11 1", "0.20 0.16 0.14 1"),
    ("0.20 0.17 0.14 1", "0.25 0.21 0.18 1"),
    ("0.24 0.21 0.18 1", "0.30 0.26 0.22 1"),
    ("0.28 0.24 0.20 1", "0.34 0.29 0.25 1"),
]

WALL_AMB, WALL_DIFF = "0.28 0.25 0.22 1", "0.32 0.28 0.25 1"
FLOOR_AMB, FLOOR_DIFF = "0.18 0.16 0.14 1", "0.22 0.19 0.17 1"
SPEC = "0.04 0.04 0.04 1"


def mat(ambient, diffuse, emissive=None):
    lines = [
        "          <material>",
        f"            <ambient>{ambient}</ambient>",
        f"            <diffuse>{diffuse}</diffuse>",
        f"            <specular>{SPEC}</specular>",
    ]
    if emissive:
        lines.append(f"            <emissive>{emissive}</emissive>")
    lines.append("          </material>")
    return lines


def box_col_vis(name, size, pose, ambient, diffuse, emissive=None, collision=True, visual=True):
    lines = []
    if collision:
        lines += [
            f"        <collision name=\"{name}_col\">",
            f"          <pose>{pose}</pose>",
            f"          <geometry><box><size>{size}</size></box></geometry>",
            "        </collision>",
        ]
    if visual:
        lines += [
            f"        <visual name=\"{name}_vis\">",
            f"          <pose>{pose}</pose>",
            f"          <geometry><box><size>{size}</size></box></geometry>",
            *mat(ambient, diffuse, emissive),
            "        </visual>",
        ]
    return lines


def cyl_vis(name, radius, length, pose, ambient, diffuse):
    """Cilindro só visual — abóbada curva contínua (eixo ao longo de X)."""
    return [
        f"        <visual name=\"{name}_vis\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><cylinder><radius>{radius}</radius><length>{length}</length></cylinder></geometry>",
        *mat(ambient, diffuse),
        "        </visual>",
    ]


def box_tunnel_segment(name, cx, cy, yaw, length, width, height, wall_t):
    """Túnel: colisão em caixa + abóbada curva visual (cilindro horizontal)."""
    lines = [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{cx} {cy} 0 0 0 {yaw}</pose>",
        "      <link name=\"link\">",
        # Piso plano
        *box_col_vis(
            "floor", f"{length} {width} {FLOOR_THICK}",
            f"0 0 {-FLOOR_THICK / 2} 0 0 0", FLOOR_AMB, FLOOR_DIFF,
        ),
        # Colisão do teto (plano, invisível ao jogador)
        *box_col_vis(
            "ceil_col", f"{length} {width} {wall_t}",
            f"0 0 {height - wall_t / 2} 0 0 0", WALL_AMB, WALL_DIFF,
            collision=True, visual=False,
        ),
        # Paredes laterais — só colisão (o cilindro visual dá a curvatura)
        *box_col_vis(
            "wall_l", f"{length} {wall_t} {height}",
            f"0 {width / 2} {height / 2} 0 0 0", WALL_AMB, WALL_DIFF,
            collision=True, visual=False,
        ),
        *box_col_vis(
            "wall_r", f"{length} {wall_t} {height}",
            f"0 {-width / 2} {height / 2} 0 0 0", WALL_AMB, WALL_DIFF,
            collision=True, visual=False,
        ),
        # Abóbada curva contínua (meio-cilindro): cilindro com eixo em X, centro em z=R
        *cyl_vis(
            "vault", R + wall_t / 2, length,
            f"0 0 {R} 0 {math.pi / 2} 0", WALL_AMB, WALL_DIFF,
        ),
        "      </link>",
        "    </model>",
        "",
    ]
    return lines


def rock_model(name, x, y, z, roll, pitch, yaw, sx, sy, sz, shade=2):
    amb, diff = ROCK_SHADES[shade % len(ROCK_SHADES)]
    return [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{x} {y} {z} {roll} {pitch} {yaw}</pose>",
        "      <link name=\"link\">",
        *box_col_vis("rock", f"{sx} {sy} {sz}", f"0 0 {sz / 2} 0 0 0", amb, diff),
        "      </link>",
        "    </model>",
        "",
    ]


def sparse_rocks(rng):
    """Poucas rochas — textura vulcânica sem poluir o túnel."""
    rocks = []
    # 1 saliente por segmento, alternando lado
    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        along = rng.uniform(-2.0, 2.0)
        side = 1.6 if i % 2 == 0 else -1.6
        wx = cx + along * math.cos(yaw) - side * math.sin(yaw) * 0.1
        wy = cy + along * math.sin(yaw) + side * math.cos(yaw) * 0.1
        rocks.extend(rock_model(
            f"wall_rock_{i}", wx, wy, rng.uniform(0.3, 1.2),
            0, 0, yaw + rng.uniform(-0.2, 0.2),
            rng.uniform(0.3, 0.55), rng.uniform(0.2, 0.35), rng.uniform(0.2, 0.4),
            shade=i % 4,
        ))
    # Pedras esparsas no chão
    for i, (x, y, yaw, sx, sy, sz) in enumerate([
        (10, 0.4, 0.1, 0.4, 0.3, 0.15),
        (24, -0.6, -0.2, 0.5, 0.35, 0.18),
        (40, 0.5, 0.3, 0.35, 0.28, 0.12),
    ]):
        rocks.extend(rock_model(f"floor_rock_{i}", x, y, 0, 0, 0, yaw, sx, sy, sz, i))
    # Alcova
    for i in range(3):
        rocks.extend(rock_model(
            f"alcove_rock_{i}", 32 + rng.uniform(-0.5, 0.5), 13 + i * 0.4, 0,
            0, 0, rng.uniform(0, 1), 0.5, 0.4, 0.2, 2,
        ))
    # Câmara — poucos detritos
    for i, (dx, dy) in enumerate([(-3, 2), (2, -3), (4, 3), (-2, -4)]):
        rocks.extend(rock_model(
            f"chamber_rock_{i}", 54 + dx, 4 + dy, 0,
            0, 0, rng.uniform(0, 2), 0.6, 0.5, 0.2, i,
        ))
    return rocks


def chamber():
    cw, cd, ch = 14.0, 12.0, 4.0
    return [
        "    <model name=\"chamber\">",
        "      <static>true</static>",
        "      <pose>54.0 4.0 0 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_col_vis("cf", f"{cw} {cd} {FLOOR_THICK}", f"0 0 {-FLOOR_THICK / 2} 0 0 0", FLOOR_AMB, FLOOR_DIFF),
        *box_col_vis("cc", f"{cw} {cd} {FLOOR_THICK}", f"0 0 {ch - FLOOR_THICK / 2} 0 0 0", WALL_AMB, WALL_DIFF, collision=True, visual=False),
        *cyl_vis("chamber_vault", 6.5, 12.0, f"0 0 5.5 0 {math.pi / 2} 0", WALL_AMB, WALL_DIFF),
        *box_col_vis("cwl", f"{T} {cd} {ch}", f"{-cw / 2} 0 {ch / 2} 0 0 0", WALL_AMB, WALL_DIFF, collision=True, visual=False),
        *box_col_vis("cwr", f"{T} {cd} {ch}", f"{cw / 2} 0 {ch / 2} 0 0 0", WALL_AMB, WALL_DIFF, collision=True, visual=False),
        *box_col_vis("cwb", f"{cw} {T} {ch}", f"0 {-cd / 2} {ch / 2} 0 0 0", WALL_AMB, WALL_DIFF, collision=True, visual=False),
        *box_col_vis("csky_l", f"4 {cd} {FLOOR_THICK}", f"-5 0 {ch - FLOOR_THICK / 2} 0 0 0", WALL_AMB, WALL_DIFF),
        *box_col_vis("csky_r", f"4 {cd} {FLOOR_THICK}", f"5 0 {ch - FLOOR_THICK / 2} 0 0 0", WALL_AMB, WALL_DIFF),
        "      </link>",
        "    </model>",
        "",
    ]


def artifacts():
    e = SPEC
    lines = []
    for rm in (
        rock_model("rubble_0", 49, 7, 0, 0, 0, 0, 1.2, 0.8, 0.4, 3),
        rock_model("rubble_1", 51, 6, 0, 0, 0, 0.3, 0.9, 0.6, 0.35, 2),
        rock_model("rubble_2", 50, 8, 0, 0, 0, 0.6, 0.7, 0.7, 0.5, 3),
        rock_model("rubble_3", 52, 7.5, 0, 0, 0, 0.9, 1.0, 0.5, 0.3, 2),
    ):
        lines.extend(rm)
    lines += [
        "    <model name=\"ancient_lander\">",
        "      <static>true</static>",
        "      <pose>55 2 0 0 0 0.4</pose>",
        "      <link name=\"link\">",
        *box_col_vis("body", "2.8 2.0 0.7", "0 0 0.35 0 0 0", "0.22 0.28 0.24 1", "0.28 0.34 0.30 1"),
        *box_col_vis("dome", "1.2 1.2 0.5", "0.6 0 0.85 0 0 0", "0.18 0.22 0.26 1", "0.24 0.30 0.34 1"),
        *box_col_vis("leg1", "0.15 0.15 0.9", "1.0 0.8 0.2 0.8 0 0.5", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        *box_col_vis("leg2", "0.15 0.15 0.7", "-1.1 -0.7 0.15 0.6 0 -0.3", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        *box_col_vis("leg3", "0.15 0.15 0.5", "0.5 -0.9 0.1 0.5 0.4 0", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_dish\">",
        "      <static>true</static>",
        "      <pose>53.5 0.5 0 0 0.5 0.8</pose>",
        "      <link name=\"link\">",
        "        <collision name=\"mast_col\"><pose>0 0 1.1 0 0 0</pose>",
        "          <geometry><cylinder><radius>0.06</radius><length>2.2</length></cylinder></geometry></collision>",
        "        <visual name=\"mast_vis\"><pose>0 0 1.1 0 0 0</pose>",
        "          <geometry><cylinder><radius>0.06</radius><length>2.2</length></cylinder></geometry>",
        *mat("0.20 0.24 0.22 1", "0.26 0.30 0.28 1"),
        "        </visual>",
        "        <collision name=\"dish_col\"><pose>0.3 0 2.0 1.2 0 0</pose>",
        "          <geometry><cylinder><radius>1.1</radius><length>0.06</length></cylinder></geometry></collision>",
        "        <visual name=\"dish_vis\"><pose>0.3 0 2.0 1.2 0 0</pose>",
        "          <geometry><cylinder><radius>1.1</radius><length>0.06</length></cylinder></geometry>",
        *mat("0.24 0.28 0.30 1", "0.30 0.34 0.36 1"),
        "        </visual>",
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"solar_debris_0\">",
        "      <static>true</static>",
        "      <pose>56.5 1.5 0 0 0.3 0.6</pose>",
        "      <link name=\"link\">",
        *box_col_vis("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"solar_debris_1\">",
        "      <static>true</static>",
        "      <pose>54 -0.5 0 0 0.3 -0.4</pose>",
        "      <link name=\"link\">",
        *box_col_vis("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_beacon\">",
        "      <static>true</static>",
        "      <pose>56 3.5 0 0 0 0</pose>",
        "      <link name=\"link\">",
        "        <collision name=\"pedestal_col\"><pose>0 0 0.3 0 0 0</pose>",
        "          <geometry><cylinder><radius>0.25</radius><length>0.6</length></cylinder></geometry></collision>",
        "        <visual name=\"pedestal_vis\"><pose>0 0 0.3 0 0 0</pose>",
        "          <geometry><cylinder><radius>0.25</radius><length>0.6</length></cylinder></geometry>",
        *mat("0.30 0.32 0.28 1", "0.36 0.38 0.34 1"),
        "        </visual>",
        "        <collision name=\"orb_col\"><pose>0 0 0.75 0 0 0</pose>",
        "          <geometry><sphere><radius>0.18</radius></sphere></geometry></collision>",
        "        <visual name=\"orb_vis\"><pose>0 0 0.75 0 0 0</pose>",
        "          <geometry><sphere><radius>0.18</radius></sphere></geometry>",
        *mat("0.0 0.3 0.4 1", "0.0 0.5 0.6 1", "0.0 0.8 1.0 1"),
        "        </visual>",
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_plaque\">",
        "      <static>true</static>",
        "      <pose>57.2 5 0 0 0 -0.3</pose>",
        "      <link name=\"link\">",
        *box_col_vis("slab", "0.08 1.0 1.4", "0 0 0.7 0 0 0", "0.12 0.14 0.16 1", "0.18 0.20 0.24 1", "0.02 0.08 0.12 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"mystery_pyramid\">",
        "      <static>true</static>",
        "      <pose>58 6 0 0 0 0.785</pose>",
        "      <link name=\"link\">",
        *box_col_vis("t0", "2.0 2.0 0.3", "0 0 0.15 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_col_vis("t1", "1.5 1.5 0.3", "0 0 0.45 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_col_vis("t2", "1.0 1.0 0.3", "0 0 0.75 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_col_vis("t3", "0.5 0.5 0.3", "0 0 1.05 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        "      </link>",
        "    </model>",
        "",
    ]
    return lines


def main():
    rng = random.Random(42)
    parts = [
        '<?xml version="1.0" ?>',
        "<!-- lava_tube.world — meio-cilindro suave (cilindro visual) + colisão em caixa.",
        "     Sem estalactites. Gerado por worlds/generate_lava_tube.py -->",
        '<sdf version="1.8">',
        '  <world name="lava_tube">',
        "",
        '    <plugin name="gz::sim::systems::Physics" filename="gz-sim-physics-system"/>',
        '    <plugin name="gz::sim::systems::UserCommands" filename="gz-sim-user-commands-system"/>',
        '    <plugin name="gz::sim::systems::SceneBroadcaster" filename="gz-sim-scene-broadcaster-system"/>',
        '    <plugin name="gz::sim::systems::Sensors" filename="gz-sim-sensors-system">',
        "      <render_engine>ogre2</render_engine>",
        "    </plugin>",
        "",
        "    <gravity>0 0 -1.62</gravity>",
        "    <magnetic_field>0 0 0</magnetic_field>",
        '    <atmosphere type="adiabatic"/>',
        '    <physics type="ode">',
        "      <max_step_size>0.002</max_step_size>",
        "      <real_time_factor>1</real_time_factor>",
        "    </physics>",
        "",
        "    <scene>",
        "      <ambient>0.06 0.06 0.10 1</ambient>",
        "      <background>0.02 0.02 0.05 1</background>",
        "      <shadows>false</shadows>",
        "    </scene>",
        "",
        '    <light name="tunnel_a" type="point">',
        "      <pose>12 0 2.0 0 0 0</pose>",
        "      <diffuse>0.35 0.32 0.28 1</diffuse>",
        "      <attenuation><range>18</range></attenuation>",
        "    </light>",
        '    <light name="tunnel_b" type="point">',
        "      <pose>30 1 2.0 0 0 0</pose>",
        "      <diffuse>0.30 0.28 0.25 1</diffuse>",
        "      <attenuation><range>18</range></attenuation>",
        "    </light>",
        '    <light name="skylight" type="directional">',
        "      <pose>50 6 8 0 0.6 0</pose>",
        "      <diffuse>0.15 0.14 0.18 1</diffuse>",
        "      <direction>0.2 -0.3 -1</direction>",
        "      <cast_shadows>false</cast_shadows>",
        "    </light>",
        '    <light name="chamber_glow" type="point">',
        "      <pose>54 4 3.2 0 0 0</pose>",
        "      <diffuse>0.25 0.35 0.45 1</diffuse>",
        "      <attenuation><range>22</range></attenuation>",
        "    </light>",
        '    <light name="beacon_pulse" type="point">',
        "      <pose>56 3.5 1.2 0 0 0</pose>",
        "      <diffuse>0.05 0.55 0.65 1</diffuse>",
        "      <attenuation><range>6</range></attenuation>",
        "    </light>",
        "",
        '    <model name="lunar_surface">',
        "      <static>true</static>",
        "      <pose>-8 0 -0.1 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_col_vis("surface", "30 40 0.2", "0 0 0 0 0 0", *ROCK_SHADES[0]),
        "      </link>",
        "    </model>",
        "",
    ]

    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        parts.extend(box_tunnel_segment(f"tube_seg_{i:02d}", cx, cy, yaw, SEG_LEN, W, H, T))

    parts.extend(box_tunnel_segment("alcove", 32, 8, 1.5708, 10.0, 3.0, H, T))
    parts.extend(chamber())
    parts.extend(sparse_rocks(rng))
    parts.extend(artifacts())

    parts += ["  </world>", "</sdf>", ""]
    content = "\n".join(parts)
    OUT.write_text(content)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {content.count('<model name=')} models)")


if __name__ == "__main__":
    main()