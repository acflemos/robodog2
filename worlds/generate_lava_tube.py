#!/usr/bin/env python3
"""Gera worlds/lava_tube.world — lava tube lunar em meio-cilindro (Hawaii-style)."""

import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "lava_tube.world"

R = 2.0          # raio interior do arco (largura útil ≈ 4 m)
T = 0.15         # espessura da rocha
N_ARCH = 14      # segmentos do arco (semicírculo)
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

# (x, y, z, roll, pitch, yaw, sx, sy, sz, shade)
ROCK_SHADES = [
    ("0.16 0.13 0.11 1", "0.20 0.16 0.14 1"),
    ("0.20 0.17 0.14 1", "0.25 0.21 0.18 1"),
    ("0.24 0.21 0.18 1", "0.30 0.26 0.22 1"),
    ("0.28 0.24 0.20 1", "0.34 0.29 0.25 1"),
]


def mat_xml(ambient, diffuse, emissive=None):
    lines = [
        "          <material>",
        f"            <ambient>{ambient}</ambient>",
        f"            <diffuse>{diffuse}</diffuse>",
        "            <specular>0.04 0.04 0.04 1</specular>",
    ]
    if emissive:
        lines.append(f"            <emissive>{emissive}</emissive>")
    lines.append("          </material>")
    return lines


def box_elem(name, size, pose, ambient, diffuse, emissive=None):
    lines = [
        f"        <collision name=\"{name}_col\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><box><size>{size}</size></box></geometry>",
        "        </collision>",
        f"        <visual name=\"{name}_vis\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><box><size>{size}</size></box></geometry>",
    ]
    lines.extend(mat_xml(ambient, diffuse, emissive))
    lines.append("        </visual>")
    return lines


def cyl_elem(name, radius, length, pose, ambient, diffuse):
    return [
        f"        <collision name=\"{name}_col\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><cylinder><radius>{radius}</radius><length>{length}</length></cylinder></geometry>",
        "        </collision>",
        f"        <visual name=\"{name}_vis\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><cylinder><radius>{radius}</radius><length>{length}</length></cylinder></geometry>",
        *mat_xml(ambient, diffuse),
        "        </visual>",
    ]


def sphere_elem(name, radius, pose, ambient, diffuse, emissive=None):
    return [
        f"        <collision name=\"{name}_col\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><sphere><radius>{radius}</radius></sphere></geometry>",
        "        </collision>",
        f"        <visual name=\"{name}_vis\">",
        f"          <pose>{pose}</pose>",
        f"          <geometry><sphere><radius>{radius}</radius></sphere></geometry>",
        *mat_xml(ambient, diffuse, emissive),
        "        </visual>",
    ]


def arch_segments(length, radius, n_arch, wall_amb, wall_diff, prefix="arch"):
    """Arco em meio-cilindro: piso plano em z=0, paredes curvas (sem estalactites)."""
    elems = []
    for i in range(n_arch):
        t1 = math.pi + i * math.pi / n_arch
        t2 = math.pi + (i + 1) * math.pi / n_arch
        tm = (t1 + t2) / 2.0
        arc_w = radius * (t2 - t1) * 1.15 + T
        y_c = (radius + T / 2) * math.sin(tm)
        z_c = radius + (radius + T / 2) * math.cos(tm)
        yaw = tm - math.pi / 2
        pose = f"0 {y_c:.4f} {z_c:.4f} 0 0 {yaw:.4f}"
        size = f"{length} {arc_w:.4f} {T}"
        elems.extend(box_elem(f"{prefix}_{i}", size, pose, wall_amb, wall_diff))
    return elems


def half_cylinder_tunnel(name, cx, cy, yaw, length, radius, n_arch, floor_w=None):
    """Segmento de túnel: chão plano + abóbada curva."""
    if floor_w is None:
        floor_w = 2 * radius
    wa, wd = ROCK_SHADES[1]
    fa, fd = ROCK_SHADES[0]
    lines = [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{cx} {cy} 0 0 0 {yaw}</pose>",
        "      <link name=\"link\">",
        *box_elem(
            "floor",
            f"{length} {floor_w} {FLOOR_THICK}",
            f"0 0 {-FLOOR_THICK / 2} 0 0 0",
            fa,
            fd,
        ),
        *arch_segments(length, radius, n_arch, wa, wd),
        "      </link>",
        "    </model>",
        "",
    ]
    return lines


def rock_model(name, x, y, z, roll, pitch, yaw, sx, sy, sz, shade=2):
    amb, diff = ROCK_SHADES[shade % len(ROCK_SHADES)]
    cz = z + sz / 2
    return [
        f"    <model name=\"{name}\">",
        "      <static>true</static>",
        f"      <pose>{x} {y} {z} {roll} {pitch} {yaw}</pose>",
        "      <link name=\"link\">",
        *box_elem("rock", f"{sx} {sy} {sz}", f"0 0 {sz / 2} 0 0 0", amb, diff),
        "      </link>",
        "    </model>",
        "",
    ]


def wall_outcrop(name, x, y, z, yaw, sx, sy, sz, shade=3):
    """Rocha vulcânica saliente na parede curva (não estalactite)."""
    return rock_model(name, x, y, z, 0, 0.15, yaw, sx, sy, sz, shade)


def generate_rocks(rng):
    rocks = []
    # Salientes nas paredes curvas ao longo do túnel
    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        for j in range(3):
            along = rng.uniform(-SEG_LEN / 2 + 0.8, SEG_LEN / 2 - 0.8)
            side = 1 if j % 2 == 0 else -1
            # posição aproximada na parede curva (meio da curva lateral)
            angle = math.pi + rng.uniform(0.35, 0.65) * math.pi
            wy = cy + along * math.sin(yaw) + side * (R - 0.25) * abs(math.sin(angle))
            wx = cx + along * math.cos(yaw)
            wz = R + R * math.cos(angle) - 0.1
            rocks.extend(
                wall_outcrop(
                    f"wall_rock_{i}_{j}",
                    wx,
                    wy,
                    wz,
                    yaw + rng.uniform(-0.4, 0.4),
                    rng.uniform(0.35, 0.7),
                    rng.uniform(0.25, 0.5),
                    rng.uniform(0.2, 0.45),
                    shade=rng.randint(0, 3),
                )
            )
    # Pedras no chão do túnel
    floor_specs = [
        (6, 0.3, 0.0, 0.2, 0.35, 0.25, 0.18),
        (14, -0.5, 0.0, -0.3, 0.5, 0.35, 0.22),
        (22, 0.8, 0.0, 0.5, 0.45, 0.3, 0.2),
        (30, -0.3, 0.0, 0.0, 0.55, 0.4, 0.25),
        (38, 0.6, 0.0, -0.4, 0.4, 0.28, 0.16),
        (46, -0.7, 0.0, 0.3, 0.5, 0.32, 0.2),
        (18, -1.2, 0.0, 0.8, 0.3, 0.22, 0.15),
        (34, 1.4, 0.0, -0.6, 0.38, 0.26, 0.17),
    ]
    for i, (x, y, z, yaw, sx, sy, sz) in enumerate(floor_specs):
        rocks.extend(rock_model(f"floor_rock_{i}", x, y, z, 0, 0, yaw, sx, sy, sz, i % 4))
    # Alcova — pilha de rochas no fundo
    for i in range(5):
        rocks.extend(
            rock_model(
                f"alcove_rock_{i}",
                32 + rng.uniform(-1, 1),
                12 + rng.uniform(-1, 1),
                0,
                rng.uniform(0, 0.3),
                rng.uniform(0, 0.2),
                rng.uniform(0, 3.14),
                rng.uniform(0.4, 0.9),
                rng.uniform(0.3, 0.7),
                rng.uniform(0.15, 0.35),
                rng.randint(1, 3),
            )
        )
    # Câmara — detritos vulcânicos espalhados
    for i in range(6):
        rocks.extend(
            rock_model(
                f"chamber_rock_{i}",
                52 + rng.uniform(-4, 4),
                4 + rng.uniform(-4, 4),
                0,
                rng.uniform(0, 0.4),
                rng.uniform(0, 0.15),
                rng.uniform(0, 3.14),
                rng.uniform(0.5, 1.1),
                rng.uniform(0.4, 0.8),
                rng.uniform(0.12, 0.3),
                rng.randint(0, 3),
            )
        )
    return rocks


def chamber_model():
    """Câmara final: abóbada curva ampla (meio-cilindro maior)."""
    cr = 5.0
    cw, cd = 14.0, 12.0
    wa, wd = ROCK_SHADES[2]
    fa, fd = ROCK_SHADES[0]
    lines = [
        "    <model name=\"chamber\">",
        "      <static>true</static>",
        "      <pose>54.0 4.0 0 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_elem("cf", f"{cw} {cd} {FLOOR_THICK}", f"0 0 {-FLOOR_THICK / 2} 0 0 0", fa, fd),
    ]
    # Abóbada longitudinal em 3 secções (frente aberta para o túnel)
    for i, x_off in enumerate([-3.5, 0.0, 3.5]):
        lines.extend(arch_segments(4.5, cr, 16, wa, wd, prefix=f"vault_{i}"))
        for j, elem in enumerate(lines):
            pass
    # Re-posicionar vault segments at x offsets — rebuild properly
    lines = [
        "    <model name=\"chamber\">",
        "      <static>true</static>",
        "      <pose>54.0 4.0 0 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_elem("cf", f"{cw} {cd} {FLOOR_THICK}", f"0 0 {-FLOOR_THICK / 2} 0 0 0", fa, fd),
    ]
    for i, x_off in enumerate([-4.0, 0.0, 4.0]):
        for arch in arch_segments(4.0, cr, 16, wa, wd, prefix=f"v{i}"):
            if "<pose>" in arch and arch.strip().startswith("<pose>"):
                pass
        # inject x offset into arch segment poses
        arch_lines = arch_segments(4.2, cr, 16, wa, wd, prefix=f"v{i}")
        patched = []
        for al in arch_lines:
            if "<pose>" in al:
                parts = al.split()
                x_val = float(parts[1]) + x_off
                parts[1] = f"{x_val:.4f}"
                al = " ".join(parts).replace("<pose>", "<pose>").replace("</pose>", "</pose>")
                if "<pose>" in al:
                    al = al.replace(f"<pose>0 ", f"<pose>{x_off} ")
            patched.append(al)
        lines.extend(patched)
    # Parede fundeira curva (fecho parcial)
    lines.extend(arch_segments(cd, cr, 16, wa, wd, prefix="back"))
    for j in range(len(lines)):
        if "back_" in lines[j] and "<pose>" in lines[j]:
            lines[j] = lines[j].replace("<pose>0 ", "<pose>7.0 ")
            lines[j] = lines[j].replace(f" {SEG_LEN}", f" {cd}")
    # Skylight — blocos de teto parcialmente colapsado
    lines.extend(
        box_elem("csky_l", f"4 {cd} {FLOOR_THICK}", f"-5 0 {cr + 0.1} 0 0 0", *ROCK_SHADES[1])
    )
    lines.extend(
        box_elem("csky_r", f"4 {cd} {FLOOR_THICK}", f"5 0 {cr + 0.1} 0 0 0", *ROCK_SHADES[1])
    )
    lines += ["      </link>", "    </model>", ""]
    return lines


def fix_arch_length(elems, length, x_offset=0.0):
    """Aplica comprimento e offset X num bloco de arch_segments."""
    out = []
    prefix = None
    for line in elems:
        if "<collision name=\"" in line:
            prefix = line.split('"')[1].replace("_col", "")
        if "<pose>" in line and "0 " in line:
            parts = line.strip().split()
            # <pose>0 y z r p y
            idx = parts.index("<pose>") + 1 if "<pose>" in parts[0] else 1
            if parts[0] == "<pose>":
                y, z = parts[2], parts[3]
                rest = " ".join(parts[4:])
                line = f"          <pose>{x_offset} {y} {z} {rest}"
            elif parts[0].startswith("<pose>"):
                inner = parts[0][6:]
                y, z = parts[1], parts[2]
                rest = " ".join(parts[3:])
                line = f"          <pose>{x_offset} {inner} {y} {z} {rest}"
        if "<size>" in line and prefix and prefix.split("_")[0] in ("v0", "v1", "v2", "back", "arch"):
            parts = line.split("<size>")[1].split("</size>")[0].split()
            if len(parts) == 3:
                line = line.replace(f"<size>{' '.join(parts)}</size>", f"<size>{length} {parts[1]} {parts[2]}</size>")
        out.append(line)
    return out


def build_chamber():
    cr = 5.0
    cd = 12.0
    wa, wd = ROCK_SHADES[2]
    fa, fd = ROCK_SHADES[0]
    lines = [
        "    <model name=\"chamber\">",
        "      <static>true</static>",
        "      <pose>54.0 4.0 0 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_elem("cf", f"14.0 {cd} {FLOOR_THICK}", f"0 0 {-FLOOR_THICK / 2} 0 0 0", fa, fd),
    ]
    for i, x_off in enumerate([-4.0, 0.0, 4.0]):
        arch = arch_segments(4.0, cr, 16, wa, wd, prefix=f"vault{i}")
        for a in arch:
            if "          <pose>" in a:
                vals = a.split("<pose>")[1].split("</pose>")[0].split()
                a = f"          <pose>{x_off} {vals[1]} {vals[2]} {vals[3]} {vals[4]} {vals[5]}</pose>"
            if "<size>" in a:
                sz = a.split("<size>")[1].split("</size>")[0].split()
                a = a.replace(f"<size>{' '.join(sz)}</size>", f"<size>4.0 {sz[1]} {sz[2]}</size>")
            lines.append(a)
    # Fundo: arco transversal
    back_arch = arch_segments(0.8, cr, 16, wa, wd, prefix="back")
    for a in back_arch:
        if "          <pose>" in a:
            vals = a.split("<pose>")[1].split("</pose>")[0].split()
            a = f"          <pose>7.0 {vals[1]} {vals[2]} {vals[3]} {vals[4]} {vals[5]}</pose>"
        if "<size>" in a:
            sz = a.split("<size>")[1].split("</size>")[0].split()
            a = a.replace(f"<size>{' '.join(sz)}</size>", f"<size>0.8 {sz[1]} {sz[2]}</size>")
        lines.append(a)
    lines.extend(box_elem("csky_l", f"4 {cd} {FLOOR_THICK}", f"-5 0 {cr} 0 0 0", *ROCK_SHADES[1]))
    lines.extend(box_elem("csky_r", f"4 {cd} {FLOOR_THICK}", f"5 0 {cr} 0 0 0", *ROCK_SHADES[1]))
    lines += ["      </link>", "    </model>", ""]
    return lines


def artifact_models():
    """Zona do enigma — inalterada em narrativa."""
    e = "0.05 0.05 0.05 1"
    lines = []
    for rm in (
        rock_model("rubble_0", 49, 7, 0.0, 0, 0, 0.0, 1.2, 0.8, 0.4, 3),
        rock_model("rubble_1", 51, 6, 0.0, 0, 0, 0.3, 0.9, 0.6, 0.35, 2),
        rock_model("rubble_2", 50, 8, 0.0, 0, 0, 0.6, 0.7, 0.7, 0.5, 3),
        rock_model("rubble_3", 52, 7.5, 0.0, 0, 0, 0.9, 1.0, 0.5, 0.3, 2),
    ):
        lines.extend(rm)
    lines.extend([
            "    <model name=\"ancient_lander\">",
            "      <static>true</static>",
            "      <pose>55 2 0 0 0 0.4</pose>",
            "      <link name=\"link\">",
            *box_elem("body", "2.8 2.0 0.7", "0 0 0.35 0 0 0", "0.22 0.28 0.24 1", "0.28 0.34 0.30 1", e),
            *box_elem("dome", "1.2 1.2 0.5", "0.6 0 0.85 0 0 0", "0.18 0.22 0.26 1", "0.24 0.30 0.34 1", e),
            *box_elem("leg1", "0.15 0.15 0.9", "1.0 0.8 0.2 0.8 0 0.5", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1", e),
            *box_elem("leg2", "0.15 0.15 0.7", "-1.1 -0.7 0.15 0.6 0 -0.3", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1", e),
            *box_elem("leg3", "0.15 0.15 0.5", "0.5 -0.9 0.1 0.5 0.4 0", "0.25 0.30 0.26 1", "0.30 0.35 0.30 1", e),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"ancient_dish\">",
            "      <static>true</static>",
            "      <pose>53.5 0.5 0 0 0.5 0.8</pose>",
            "      <link name=\"link\">",
            *cyl_elem("mast", 0.06, 2.2, "0 0 1.1 0 0 0", "0.20 0.24 0.22 1", "0.26 0.30 0.28 1"),
            *cyl_elem("dish", 1.1, 0.06, "0.3 0 2.0 1.2 0 0", "0.24 0.28 0.30 1", "0.30 0.34 0.36 1"),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"solar_debris_0\">",
            "      <static>true</static>",
            "      <pose>56.5 1.5 0 0 0.3 0.6</pose>",
            "      <link name=\"link\">",
            *box_elem("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1", e),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"solar_debris_1\">",
            "      <static>true</static>",
            "      <pose>54 -0.5 0 0 0.3 -0.4</pose>",
            "      <link name=\"link\">",
            *box_elem("panel", "1.8 0.9 0.04", "0 0 0.15 0 0 0", "0.15 0.18 0.22 1", "0.20 0.24 0.30 1", e),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"ancient_beacon\">",
            "      <static>true</static>",
            "      <pose>56 3.5 0 0 0 0</pose>",
            "      <link name=\"link\">",
            *cyl_elem("pedestal", 0.25, 0.6, "0 0 0.3 0 0 0", "0.30 0.32 0.28 1", "0.36 0.38 0.34 1"),
            *sphere_elem("orb", 0.18, "0 0 0.75 0 0 0", "0.0 0.3 0.4 1", "0.0 0.5 0.6 1", "0.0 0.8 1.0 1"),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"ancient_plaque\">",
            "      <static>true</static>",
            "      <pose>57.2 5 0 0 0 -0.3</pose>",
            "      <link name=\"link\">",
            *box_elem("slab", "0.08 1.0 1.4", "0 0 0.7 0 0 0", "0.12 0.14 0.16 1", "0.18 0.20 0.24 1", "0.02 0.08 0.12 1"),
            "      </link>",
            "    </model>",
            "",
            "    <model name=\"mystery_pyramid\">",
            "      <static>true</static>",
            "      <pose>58 6 0 0 0 0.785</pose>",
            "      <link name=\"link\">",
            *box_elem("t0", "2.0 2.0 0.3", "0 0 0.15 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1", e),
            *box_elem("t1", "1.5 1.5 0.3", "0 0 0.45 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1", e),
            *box_elem("t2", "1.0 1.0 0.3", "0 0 0.75 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1", e),
            *box_elem("t3", "0.5 0.5 0.3", "0 0 1.05 0 0 0", "0.14 0.12 0.10 1", "0.18 0.15 0.13 1", e),
            "      </link>",
            "    </model>",
            "",
    ])
    return lines


def main():
    rng = random.Random(42)
    parts = [
        '<?xml version="1.0" ?>',
        "<!-- lava_tube.world — Lava tube lunar estilo Hawaii: meio-cilindro (piso plano +",
        "     paredes curvas), rocha vulcânica nas laterais. Sem estalactites (Lua sem água).",
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
        "      <ambient>0.06 0.06 0.10 1</ambient>",
        "      <background>0.02 0.02 0.05 1</background>",
        "      <shadows>false</shadows>",
        "    </scene>",
        "",
        "    <light name=\"tunnel_a\" type=\"point\">",
        "      <pose>12 0 2.0 0 0 0</pose>",
        "      <diffuse>0.35 0.32 0.28 1</diffuse>",
        "      <attenuation><range>18</range></attenuation>",
        "    </light>",
        "    <light name=\"tunnel_b\" type=\"point\">",
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
        "    <light name=\"chamber_glow\" type=\"point\">",
        "      <pose>54 4 3.5 0 0 0</pose>",
        "      <diffuse>0.25 0.35 0.45 1</diffuse>",
        "      <attenuation><range>22</range></attenuation>",
        "    </light>",
        "    <light name=\"beacon_pulse\" type=\"point\">",
        "      <pose>56 3.5 1.2 0 0 0</pose>",
        "      <diffuse>0.05 0.55 0.65 1</diffuse>",
        "      <attenuation><range>6</range></attenuation>",
        "    </light>",
        "",
        "    <model name=\"lunar_surface\">",
        "      <static>true</static>",
        "      <pose>-8 0 -0.1 0 0 0</pose>",
        "      <link name=\"link\">",
        *box_elem("surface", "30 40 0.2", "0 0 0 0 0 0", *ROCK_SHADES[0]),
        "      </link>",
        "    </model>",
        "",
    ]

    for i, (cx, cy, yaw) in enumerate(SEGMENTS):
        parts.extend(half_cylinder_tunnel(f"tube_seg_{i:02d}", cx, cy, yaw, SEG_LEN, R, N_ARCH))

    # Alcova — meio-cilindro menor, perpendicular
    parts.extend(
        half_cylinder_tunnel("alcove", 32, 8, 1.5708, 10.0, 1.5, 10, floor_w=3.0)
    )

    parts.extend(build_chamber())
    parts.extend(generate_rocks(rng))
    parts.extend(artifact_models())

    parts += ["  </world>", "</sdf>", ""]
    content = "\n".join(parts)
    OUT.write_text(content)
    n_models = content.count("<model name=")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {n_models} models)")


if __name__ == "__main__":
    main()