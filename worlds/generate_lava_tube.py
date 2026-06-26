#!/usr/bin/env python3
"""Gera worlds/lava_tube.world — lava tube lunar em caixa oca (v1.1).

Estratégia v1.1 (zona navegável parcial — robodog2):
  - Entrada semi-enterrada: túnel abaixado 1,5 m (metade da seção acima do regolito)
  - Rampa de acesso do piso lunar (z=0) ao piso interno inicial
  - Subida progressiva do piso por segmento — X3 avança e fica preso no limite das rodas
  - Câmara final e Enigma acima do nível externo — visíveis ao longe, acessíveis no robodog3
"""

import math
from pathlib import Path

OUT = Path(__file__).parent / "lava_tube.world"

SEG_LEN = 8.0
INNER_W = 4.0
INNER_H = 3.0
WALL_T = 0.2
FLOOR_T = 0.15
FLOOR_Z = -FLOOR_T / 2
CEIL_Z = INNER_H - FLOOR_T / 2
WALL_Z = INNER_H / 2

# Metade do túnel acima do regolito (z=0); piso interno na boca em z = -TUBE_BURY.
TUBE_BURY = INNER_H / 2

# Piso navegável (topo) no início de cada segmento; último valor = câmara.
SEG_FLOOR_Z = [-1.5, -1.35, -1.1, -0.75, -0.25, 0.25, 0.6]

SEGMENTS = [
    (4.0, 0.0, 0.0),
    (12.0, 0.0, 0.0),
    (20.0, 0.4, 0.08),
    (28.0, 1.2, 0.16),
    (36.0, 2.0, 0.12),
    (44.0, 2.6, 0.05),
]

FLOOR_AMB, FLOOR_DIFF = "0.18 0.16 0.14 1", "0.22 0.19 0.17 1"
CEIL_AMB, CEIL_DIFF = "0.28 0.25 0.22 1", "0.32 0.28 0.25 1"
WALL_AMB, WALL_DIFF = "0.30 0.27 0.24 1", "0.34 0.30 0.27 1"
REGOLITH_AMB, REGOLITH_DIFF = "0.20 0.18 0.16 1", "0.25 0.22 0.20 1"
CH_FLOOR_AMB, CH_FLOOR_DIFF = "0.16 0.14 0.12 1", "0.20 0.17 0.15 1"
CH_SKY_AMB, CH_SKY_DIFF = "0.22 0.20 0.18 1", "0.26 0.23 0.20 1"
SPEC = "0.05 0.05 0.05 1"
RUBBLE_AMB, RUBBLE_DIFF = "0.32 0.28 0.24 1", "0.36 0.32 0.28 1"


def mat(ambient, diffuse, specular=SPEC, emissive=None):
    lines = [
        "          <material>",
        f"            <ambient>{ambient}</ambient>",
        f"            <diffuse>{diffuse}</diffuse>",
        f"            <specular>{specular}</specular>",
    ]
    if emissive:
        lines.append(f"            <emissive>{emissive}</emissive>")
    lines.append("          </material>")
    return lines


def box_pair(prefix, size, pose, ambient, diffuse, emissive=None):
    return [
        f"        <collision name=\"{prefix}_col\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><box><size>{size}</size></box></geometry>",
        "        </collision>",
        f"        <visual name=\"{prefix}_vis\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><box><size>{size}</size></box></geometry>",
        *mat(ambient, diffuse, emissive=emissive),
        "        </visual>",
    ]


def hollow_segment(name, cx, cy, yaw, length, floor_z, width=INNER_W, height=INNER_H, end_wall=False):
    half_w = width / 2
    lines = [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{cx} {cy} {floor_z} 0 0 {yaw}</pose>",
        "      <link name=\"link\">",
        *box_pair("floor", f"{length} {width} {FLOOR_T}", f"0 0 {FLOOR_Z} 0 0 0", FLOOR_AMB, FLOOR_DIFF),
        *box_pair("ceiling", f"{length} {width} {FLOOR_T}", f"0 0 {CEIL_Z} 0 0 0", CEIL_AMB, CEIL_DIFF),
        *box_pair("wall_l", f"{length} {WALL_T} {height}", f"0 {half_w} {WALL_Z} 0 0 0", WALL_AMB, WALL_DIFF),
        *box_pair("wall_r", f"{length} {WALL_T} {height}", f"0 {-half_w} {WALL_Z} 0 0 0", WALL_AMB, WALL_DIFF),
    ]
    if end_wall:
        half = length / 2
        lines.extend(box_pair(
            "aend", f"{WALL_T} {width} {height}", f"{half} 0 {WALL_Z} 0 0 0", WALL_AMB, WALL_DIFF,
        ))
    lines += ["      </link>", "    </model>", ""]
    return lines


def entrance_ramp():
    """Rampa do regolito (z=0) ao piso do primeiro segmento (z=-1,5 m)."""
    ramp_len = 7.0
    drop = TUBE_BURY
    pitch = -math.atan2(drop, ramp_len)
    cx = -ramp_len / 2
    cz = -drop / 2
    return [
        "    <model name=\"entrance_ramp\">",
        "      <static>true</static>",
        f"      <pose>{cx} 0 {cz} 0 {pitch} 0</pose>",
        "      <link name=\"link\">",
        *box_pair(
            "ramp",
            f"{ramp_len} {INNER_W} {FLOOR_T}",
            f"0 0 {FLOOR_Z} 0 0 0",
            FLOOR_AMB,
            FLOOR_DIFF,
        ),
        "      </link>",
        "    </model>",
        "",
    ]


def entrance_berms():
    """Montes de regolito nos flancos da boca — visual semi-enterrado."""
    berms = [
        ("berm_l", 0.5, 2.6, 0.9, (3.0, 1.2, 1.8)),
        ("berm_r", 0.5, -2.6, 0.9, (3.0, 1.2, 1.8)),
        ("berm_top", 2.5, 0.0, 1.35, (5.0, 4.5, 0.7)),
    ]
    lines = []
    for name, x, y, z, size in berms:
        sx, sy, sz = size
        lines += [
            f"    <model name=\"{name}\">",
            "      <static>true</static>",
            f"      <pose>{x} {y} {z} 0 0 0</pose>",
            "      <link name=\"link\">",
            *box_pair("b", f"{sx} {sy} {sz}", f"0 0 0 0 0 0", REGOLITH_AMB, REGOLITH_DIFF),
            "      </link>",
            "    </model>",
            "",
        ]
    return lines


def wheel_barrier():
    """Degrau natural no limite da zona navegável do X3 (~entre seg 3 e 4)."""
    floor_z = SEG_FLOOR_Z[3]
    step_h = SEG_FLOOR_Z[4] - SEG_FLOOR_Z[3]
    return [
        "    <model name=\"wheel_barrier\">",
        "      <static>true</static>",
        f"      <pose>27.0 1.0 {floor_z + step_h / 2} 0 0 0.16</pose>",
        "      <link name=\"link\">",
        *box_pair(
            "lip",
            f"0.35 {INNER_W - 0.4} {step_h}",
            "0 0 0 0 0 0",
            RUBBLE_AMB,
            RUBBLE_DIFF,
        ),
        "      </link>",
        "    </model>",
        "",
    ]


def chamber():
    floor_z = SEG_FLOOR_Z[6]
    cw, cd, ch = 14.0, 12.0, 4.0
    return [
        "    <model name=\"chamber\">",
        "      <static>true</static>",
        f"      <pose>54.0 4.0 {floor_z} 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_pair("cf", f"{cw} {cd} {FLOOR_T}", f"0 0 {FLOOR_Z} 0 0 0", CH_FLOOR_AMB, CH_FLOOR_DIFF),
        *box_pair("cc", f"{cw} {cd} {FLOOR_T}", f"0 0 {ch - FLOOR_T / 2} 0 0 0", CEIL_AMB, CEIL_DIFF),
        *box_pair("cwl", f"{WALL_T} {cd} {ch}", f"{-cw / 2} 0 {ch / 2} 0 0 0", CEIL_AMB, CEIL_DIFF),
        *box_pair("cwr", f"{WALL_T} {cd} {ch}", f"{cw / 2} 0 {ch / 2} 0 0 0", CEIL_AMB, CEIL_DIFF),
        *box_pair("cwb", f"{cw} {WALL_T} {ch}", f"0 {-cd / 2} {ch / 2} 0 0 0", CEIL_AMB, CEIL_DIFF),
        *box_pair("csky_l", f"4 {cd} {FLOOR_T}", f"-5 0 {ch - FLOOR_T / 2} 0 0 0", CH_SKY_AMB, CH_SKY_DIFF),
        *box_pair("csky_r", f"4 {cd} {FLOOR_T}", f"5 0 {ch - FLOOR_T / 2} 0 0 0", CH_SKY_AMB, CH_SKY_DIFF),
        "      </link>",
        "    </model>",
        "",
    ]


def rubble(name, x, y, floor_z, yaw, size, pose_z):
    sx, sy, sz = size
    return [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{x} {y} {floor_z} 0 0 {yaw}</pose>",
        "      <link name=\"link\">",
        *box_pair("r", f"{sx} {sy} {sz}", f"0 0 {pose_z} 0 0 0", RUBBLE_AMB, RUBBLE_DIFF),
        "      </link>",
        "    </model>",
        "",
    ]


def artifacts():
    fz = SEG_FLOOR_Z[6]
    lines = []
    for args in (
        ("rubble_0", 49, 7, 0.0, (1.2, 0.8, 0.4), 0.2),
        ("rubble_1", 51, 6, 0.15, (0.9, 0.6, 0.35), 0.175),
        ("rubble_2", 50, 8, 0.25, (0.7, 0.7, 0.5), 0.25),
        ("rubble_3", 52, 7.5, 0.1, (1.0, 0.5, 0.3), 0.15),
    ):
        lines.extend(rubble(args[0], args[1], args[2], fz, args[3], args[4], args[5]))

    lines += [
        "    <model name=\"ancient_lander\">",
        "      <static>true</static>",
        f"      <pose>55 2 {fz} 0 0 0.4</pose>",
        "      <link name=\"link\">",
        *box_pair("body", "2.8 2.0 0.7", "0 0 0.35 0 0 0", "0.22 0.28 0.24 1", "0.28 0.34 0.30 1"),
        *box_pair("dome", "1.2 1.2 0.5", "0.6 0 0.85 0 0 0", "0.18 0.22 0.26 1", "0.24 0.30 0.34 1"),
        *box_pair("leg1", "0.15 0.15 0.9", "1.0 0.8 0.2 0.8 0 0.5", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        *box_pair("leg2", "0.15 0.15 0.7", "-1.1 -0.7 0.15 0.6 0 -0.3", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        *box_pair("leg3", "0.15 0.15 0.5", "0.5 -0.9 0.1 0.5 0.4 0", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_dish\">",
        "      <static>true</static>",
        f"      <pose>53.5 0.5 {fz} 0 0.5 0.8</pose>",
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
        f"      <pose>56.5 1.5 {fz} 0 0.3 0.6</pose>",
        "      <link name=\"link\">",
        *box_pair("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"solar_debris_1\">",
        "      <static>true</static>",
        f"      <pose>54 -0.5 {fz} 0 0.3 -0.4</pose>",
        "      <link name=\"link\">",
        *box_pair("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_beacon\">",
        "      <static>true</static>",
        f"      <pose>56 3.5 {fz} 0 0 0</pose>",
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
        *mat("0.0 0.3 0.4 1", "0.0 0.5 0.6 1", emissive="0.0 0.8 1.0 1"),
        "        </visual>",
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"ancient_plaque\">",
        "      <static>true</static>",
        f"      <pose>57.2 5 {fz} 0 0 -0.3</pose>",
        "      <link name=\"link\">",
        *box_pair("slab", "0.08 1.0 1.4", "0 0 0.7 0 0 0", "0.12 0.14 0.16 1", "0.18 0.20 0.24 1", emissive="0.02 0.08 0.12 1"),
        "      </link>",
        "    </model>",
        "",
        "    <model name=\"mystery_pyramid\">",
        "      <static>true</static>",
        f"      <pose>58 6 {fz} 0 0 0.785</pose>",
        "      <link name=\"link\">",
        *box_pair("t0", "2.0 2.0 0.3", "0 0 0.15 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_pair("t1", "1.5 1.5 0.3", "0 0 0.45 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_pair("t2", "1.0 1.0 0.3", "0 0 0.75 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        *box_pair("t3", "0.5 0.5 0.3", "0 0 1.05 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1"),
        "      </link>",
        "    </model>",
        "",
    ]
    return lines


def floor_z_at(x, y=0.0):
    """Interpola elevação do piso ao longo do eixo principal do túnel."""
    if x < 0:
        if x <= -7.0:
            return 0.0
        return -TUBE_BURY * (x + 7.0) / 7.0
    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        half = SEG_LEN / 2
        dx = x - cx
        dy = y - cy
        along = dx * math.cos(yaw) + dy * math.sin(yaw)
        if -half <= along <= half:
            t = (along + half) / SEG_LEN
            z0 = SEG_FLOOR_Z[i]
            z1 = SEG_FLOOR_Z[i + 1]
            return z0 + t * (z1 - z0)
    return SEG_FLOOR_Z[6]


def tunnel_lights():
    """Luzes pontuais ao longo do túnel — interior visível na câmara do Gazebo."""
    spots = [
        (-1.0, 0.0),
        (4.0, 0.0),
        (12.0, 0.0),
        (20.0, 0.4),
        (28.0, 1.2),
        (36.0, 2.0),
        (44.0, 2.6),
        (32.0, 8.0),
        (48.0, 3.0),
    ]
    lines = []
    for i, (x, y) in enumerate(spots):
        fz = floor_z_at(x, y)
        z = fz + 2.0
        lines += [
            f'    <light name="tunnel_lit_{i:02d}" type="point">',
            f"      <pose>{x} {y} {z} 0 0 0</pose>",
            "      <diffuse>0.75 0.68 0.58 1</diffuse>",
            "      <specular>0.12 0.11 0.10 1</specular>",
            "      <attenuation><range>14</range><linear>0.08</linear><constant>0.4</constant></attenuation>",
            "    </light>",
            "",
        ]
    return lines


def main():
    parts = [
        '<?xml version="1.0" ?>',
        "<!-- lava_tube.world — Lava tube lunar v1.1, gravidade 1/6g, zona navegável parcial.",
        "     Entrada semi-enterrada + rampa + subida progressiva (robodog2 / X3).",
        "     Câmara final: Enigma acima do regolito (robodog3).",
        "     Gerado por worlds/generate_lava_tube.py -->",
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
        "      <ambient>0.10 0.09 0.12 1</ambient>",
        "      <background>0.02 0.02 0.05 1</background>",
        "      <shadows>false</shadows>",
        "    </scene>",
        "",
        *tunnel_lights(),
        '    <light name="skylight" type="directional">',
        "      <pose>50 6 8 0 0.6 0</pose>",
        "      <diffuse>0.18 0.16 0.20 1</diffuse>",
        "      <direction>0.2 -0.3 -1</direction>",
        "      <cast_shadows>false</cast_shadows>",
        "    </light>",
        '    <light name="chamber_glow" type="point">',
        f"      <pose>54 4 {SEG_FLOOR_Z[6] + 2.8} 0 0 0</pose>",
        "      <diffuse>0.40 0.50 0.60 1</diffuse>",
        "      <attenuation><range>22</range><linear>0.05</linear><constant>0.5</constant></attenuation>",
        "    </light>",
        '    <light name="beacon_pulse" type="point">',
        f"      <pose>56 3.5 {SEG_FLOOR_Z[6] + 1.2} 0 0 0</pose>",
        "      <diffuse>0.10 0.70 0.80 1</diffuse>",
        "      <attenuation><range>8</range></attenuation>",
        "    </light>",
        "",
        '    <model name="lunar_surface">',
        "      <static>true</static>",
        "      <pose>-8 0 -0.1 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_pair("surface", "30 40 0.2", "0 0 0 0 0 0", REGOLITH_AMB, REGOLITH_DIFF),
        "      </link>",
        "    </model>",
        "",
        *entrance_ramp(),
        *entrance_berms(),
    ]

    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        parts.extend(hollow_segment(
            f"tube_seg_{i:02d}", cx, cy, yaw, SEG_LEN, SEG_FLOOR_Z[i],
        ))

    parts.extend(wheel_barrier())
    parts.extend(hollow_segment(
        "alcove", 32, 8, 1.5708, 10.0, SEG_FLOOR_Z[4], width=3.0, end_wall=True,
    ))
    parts.extend(chamber())
    parts.extend(artifacts())

    parts += ["  </world>", "</sdf>", ""]
    content = "\n".join(parts)
    OUT.write_text(content)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {content.count('<model name=')} models)")


if __name__ == "__main__":
    main()