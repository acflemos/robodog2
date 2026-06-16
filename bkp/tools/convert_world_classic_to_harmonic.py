#!/usr/bin/env python3
"""
Converte mundos .world do Gazebo Classic (SDF 1.6) para Gazebo Harmonic (SDF 1.8).

Problema que resolve:
  No Gazebo Classic, arquivos .world salvos pelo editor contêm um bloco <state>
  com as posições REAIS dos modelos (após movê-los no editor). As poses nas
  definições <model> são as posições originais de criação — frequentemente diferentes.
  O Gazebo Classic aplica o bloco <state> ao carregar, corrigindo as posições.
  O Gazebo Harmonic não possui esse mecanismo, então as paredes aparecem fora do lugar.

  A solução é usar as poses do bloco <state> como poses definitivas dos modelos
  no arquivo Harmonic convertido.

Uso:
  Edite as variáveis SRC, DST e STATE_POSES abaixo para o mundo que deseja converter.
  Depois execute: python3 convert_world_classic_to_harmonic.py

Histórico:
  cma_vazio.world  — convertido em 2026-06-03
  cma_moveis.world — convertido em 2026-06-04
"""

import re

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — editar para cada conversão
# ---------------------------------------------------------------------------

SRC = '/home/antonio/ros2_ws/src/robodog2/worlds/robodog1_classic/cma_moveis.world'
DST = '/home/antonio/ros2_ws/src/robodog2/worlds/cma_moveis.world'

# Poses corretas extraídas do bloco <state> do arquivo Classic
STATE_POSES = {
    "ground_plane":             "0 0 0 0 0 0",
    "cma_escritorio":           "-1.8304 1.03024 0 0 0 0",
    "cma_L2":                   "4.51683 -3.24587 0 0 0 0",
    "cma_L3":                   "6.37221 -2.26022 0 0 0 0",
    "cma_L5":                   "3.77502 1.45512 0 0 0 0",
    "cma_U":                    "4.97895 -9.92408 0 0 0 0",
    "cma_apoio_s":              "-1.31033 2.2717 -0.187436 1e-06 -1e-06 -0.000463",
    "cma_area2":                "4.52275 5.67862 0 0 0 0",
    "cma_area_a1":              "0 0 -0.135158 0 0 0",
    "cma_area_a2":              "5.2562 6.23248 0.330708 0 0 0",
    "cma_area_lixo":            "4.35576 7.00999 0.344816 5e-06 3e-06 0",
    "cma_armario":              "-0.670509 -1.58172 1e-06 -1e-06 1e-06 -0.000321",
    "cma_armario_0":            "-5.27925 -5.41641 1e-06 -1e-06 2e-06 -0.003305",
    "cma_armario_1":            "-4.70209 -9.22485 1e-06 -1e-06 2e-06 -0.003305",
    "cma_armario_2":            "-1.4424 -6.56352 2e-06 -2e-06 0 1.56237",
    "cma_armario_2_clone":      "-1.44894 -8.44643 2e-06 -2e-06 0 1.56237",
    "cma_armario_3":            "-0.942094 -5.55504 -3e-06 2e-06 0 -0.003035",
    "cma_armario_4":            "-0.785008 -6.54733 2e-06 -2e-06 0 1.56175",
    "cma_armario_5":            "-0.793528 -8.27849 2e-06 -2e-06 0 1.56639",
    "cma_armario_6":            "-4.38644 0.687217 2e-06 -2e-06 0 1.56539",
    "cma_armario_7":            "-4.38592 -1.06627 2e-06 -2e-06 0 1.56764",
    "cma_armario_coz_150x20cm": "-1.79432 0.264761 -3.7e-05 0 -5e-06 0",
    "cma_armario_coz_190x40cm": "5.29765 -0.14773 0.5 0 0 -0.000515",
    "cma_armario_coz_190x70cm": "-1.59219 0.370557 -5e-06 2e-06 0 -0.0012",
    "cma_armario_s":            "-1.63837 -3.93781 0.5 4e-06 3e-06 0.001322",
    "cma_armario_s_0":          "-5.16846 -8.01557 0.5 0 0 -1.57603",
    "cma_armario_s_1":          "-3.57948 -7.82374 0.499996 0 9e-06 -0.000452",
    "cma_banheiro":             "-5.22928 3.4871 0 0 0 0",
    "cma_banheiro_e":           "1.18358 3.89879 0 0 0 0",
    "cma_banr_a1":              "-4.17589 3.52745 0.24228 0 7e-06 4.8e-05",
    "cma_banr_b":               "-5.74657 3.47219 0.198151 0 5e-06 0",
    "cma_banr_v":               "-5.39836 3.83737 0.285921 0 0 0",
    "cma_bans_a1":              "-1.95772 0.037842 0.427992 0 2e-06 0",
    "cma_bans_b":               "-1.59754 2.06496 0.168296 0 0 0",
    "cma_bans_v":               "-1.97511 1.61732 0.320189 0 0 0",
    "cma_barra_70cm":           "-3.32572 -4.40177 -0.322102 -2.7e-05 0 -0.000962",
    "cma_barra_70cmD":          "-1.41318 -11.6476 -0.32219 5e-06 -1.2e-05 0.003978",
    "cma_barra_70cmV":          "7.29517 -1.92399 0.177863 0 -2.7e-05 -0.000724",
    "cma_bau_s":                "-2.04275 -1.48572 0.312559 3e-06 0 0.000796",
    "cma_bau_s_0":              "-2.76535 2.2429 0.312559 3e-06 0 -0.000914",
    "cma_cama_c":               "-4.43933 -6.24816 0.5 0 0 0",
    "cma_cama_c_0":             "-3.38238 1.38787 0.5 0 0 -2e-06",
    "cma_cama_s":               "0.313704 -5.42014 0.434082 0 0 -4e-06",
    "cma_cama_s_0":             "0.313026 -7.03078 0.434082 0 0 0",
    "cma_cesto":                "1.91097 1.85863 0.499998 0 0 -0.013205",
    "cma_cesto_0":              "1.10203 -6.65937 0.499999 0 0 0",
    "cma_dispensa":             "2.52584 4.40119 0 0 0 0",
    "cma_emp_a1":               "2.06895 7.13219 0.22609 0 0 0",
    "cma_emp_a2":               "2.47376 5.46593 0.33087 0 0 0",
    "cma_emp_a3":               "0.757866 5.97243 0.499999 0 -3e-06 -0.00022",
    "cma_gaveteiro":            "-0.591985 2.32618 0.499997 6e-06 6e-06 0.000429",
    "cma_gaveteiro_0":          "-0.577969 0.983863 0.500002 -1e-06 8e-06 -0.015335",
    "cma_gaveteiro_1":          "-2.68858 0.131637 0.499997 6e-06 -6e-06 -0.000698",
    "cma_gaveteiro_pequeno_0":  "-0.336168 1.39515 0 0 -7e-06 -0.000147",
    "cma_gaveteiro_pequeno_1":  "-5.43095 -6.25509 -4e-06 3e-06 -3e-06 -1.8e-05",
    "cma_gaveteiro_pequeno_2":  "-5.39165 -8.58552 -1e-06 1e-06 -1e-06 -4.3e-05",
    "cma_gaveteiro_pequeno_e":  "-0.653035 0.558766 0.5 1e-06 0 -0.015345",
    "cma_geladeira":            "5.21959 1.47716 0.499997 0 9e-06 -2.2e-05",
    "cma_lavabo":               "7.72297 -4.09302 0 0 0 0",
    "cma_lixo":                 "-1.35785 -1.52544 -5e-06 0 0 -0.543097",
    "cma_lixo_0":               "-1.60935 -0.442731 -8e-06 0 0 -0.009777",
    "cma_lixo_1":               "-2.57103 -9.7975 -3e-06 0 0 0",
    "cma_lixo_2":               "-5.27342 -2.21345 -3e-06 0 0 0",
    "cma_lixo_3":               "-4.57495 -2.209 -3e-06 0 0 0",
    "cma_lixo_4":               "3.1651 -1.9552 -8e-06 0 0 0",
    "cma_lixo_5":               "3.69005 -1.94018 -8e-06 0 0 0",
    "cma_parede_L":             "4.97628 -6.69992 0 0 0 0",
    "cma_parede_t":             "0.159955 -3.24016 0 0 0 0",
    "cma_pe_mesa2":             "0.008634 -0.342094 0.395796 0 -2e-06 -0.002168",
    "cma_picador":              "-0.583593 -5.45079 0.5 1e-06 2e-06 1.56326",
    "cma_picador_0":            "1.46993 1.36075 0.499999 0 2e-06 0.01021",
    "cma_qe":                   "1.79561 6.31228 0 0 0 0",
    "cma_quartos":              "-2.58169 -7.26456 0 0 0 0",
    "cma_sofa2":                "-0.095334 -0.408334 -5e-06 -3e-06 -1e-06 2e-06",
    "cma_sofa_2_lugares":       "1.36414 1.47316 0.5 0 0 0.000384",
    "cma_sofa_ch2":             "0.11721 2.42164 0 0 0 0",
    "cma_sui_b":                "-6.02144 -8.57086 0.323803 0 0 4.6e-05",
    "cma_sui_v":                "-6.15386 -9.87003 0.361153 -3e-06 1e-06 1e-06",
    "cma_sut_a1":               "-4.7378 -9.85675 0.322703 0 0 0",
    "cma_varanda1":             "-6.32518 -2.59313 0 0 0 0",
}

# Intervalo de linhas (0-indexed) com definições de modelos no arquivo Classic.
# cma_moveis.world: ground_plane=linhas 16-82, state=548-1747, gui=1748-1754
# Incluir: cma_escritorio [82:548] + todos os outros (após gui) [1754:fim]
MODEL_LINE_RANGES = [
    (82, 548),     # cma_escritorio
    (1754, None),  # restantes (walls + furniture)
]

# ---------------------------------------------------------------------------
# TEMPLATES FIXOS
# ---------------------------------------------------------------------------

SDF_HEADER = '''<?xml version="1.0" ?>
<sdf version="1.8">
  <world name="default">

    <plugin name="gz::sim::systems::Physics" filename="gz-sim-physics-system"/>
    <plugin name="gz::sim::systems::UserCommands" filename="gz-sim-user-commands-system"/>
    <plugin name="gz::sim::systems::SceneBroadcaster" filename="gz-sim-scene-broadcaster-system"/>
    <plugin name="gz::sim::systems::Sensors" filename="gz-sim-sensors-system">
      <render_engine>ogre2</render_engine>
    </plugin>

    <gravity>0 0 -9.8</gravity>
    <magnetic_field>6e-06 2.3e-05 -4.2e-05</magnetic_field>
    <atmosphere type="adiabatic"/>

    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
    </physics>

    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
      <shadows>true</shadows>
    </scene>

    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.1 0.1 0.1 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.5 -1</direction>
    </light>

    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>100</mu>
                <mu2>50</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.8 0.8 0.8 1</specular>
          </material>
        </visual>
      </link>
    </model>
'''

SDF_FOOTER = '''  </world>
</sdf>
'''

# ---------------------------------------------------------------------------
# LÓGICA DE CONVERSÃO
# ---------------------------------------------------------------------------

def convert_link_content(text):
    # Remove blocos Classic desnecessários (com conteúdo)
    text = re.sub(r'\s*<inertial>.*?</inertial>', '', text, flags=re.DOTALL)
    text = re.sub(r'\s*<torsional>.*?</torsional>', '', text, flags=re.DOTALL)
    text = re.sub(r'\s*<bounce>.*?</bounce>', '', text, flags=re.DOTALL)
    text = re.sub(r'\s*<contact>.*?</contact>', '', text, flags=re.DOTALL)
    text = re.sub(r'\s*<bullet>.*?</bullet>', '', text, flags=re.DOTALL)

    # Remove tags simples Classic (atributos não usados no Harmonic)
    text = re.sub(r'\s*<self_collide>\d+</self_collide>', '', text)
    text = re.sub(r'\s*<kinematic>\d+</kinematic>', '', text)
    text = re.sub(r'\s*<gravity>\d+</gravity>', '', text)
    text = re.sub(r'\s*<max_contacts>\d+</max_contacts>', '', text)
    text = re.sub(r'\s*<laser_retro>0</laser_retro>', '', text)
    text = re.sub(r'\s*<allow_auto_disable>\d+</allow_auto_disable>', '', text)
    text = re.sub(r'\s*<lighting>\d+</lighting>', '', text)
    text = re.sub(r'\s*<cast_shadows>\d+</cast_shadows>', '', text)
    text = re.sub(r'\s*<transparency>0</transparency>', '', text)
    text = re.sub(r'\s*<emissive>[^<]*</emissive>', '', text)
    text = re.sub(r'\s*<fdir1>[^<]*</fdir1>', '', text)
    text = re.sub(r'\s*<slip1>[^<]*</slip1>', '', text)
    text = re.sub(r'\s*<slip2>[^<]*</slip2>', '', text)
    text = re.sub(r'\s*<ode/>', '', text)

    # Converte material Gazebo Classic → SDF 1.8 simples
    text = re.sub(
        r'<material>.*?</material>',
        '<material>\n            <ambient>0.7 0.7 0.7 1</ambient>\n'
        '            <diffuse>0.7 0.7 0.7 1</diffuse>\n          </material>',
        text, flags=re.DOTALL
    )

    # Remove atributo frame='' das poses
    text = re.sub(r"<pose frame=''>(.*?)</pose>", r'<pose>\1</pose>', text)
    # Limpa -0 (valor inútil)
    text = re.sub(r'\b-0\b', '0', text)

    # Remove blocos vazios que sobram
    text = re.sub(r'\s*<friction>\s*</friction>', '', text)
    text = re.sub(r'\s*<surface>\s*</surface>', '', text)
    return text


def convert_model(model_name, model_text):
    new_pose = STATE_POSES.get(model_name, "0 0 0 0 0 0")
    model_text = re.sub(r"<model name='([^']+)'>", r'<model name="\1">', model_text)

    # Substitui a pose no nível do modelo (exatamente 6 espaços de indent = filho direto do model).
    # Funciona para modelos estruturais (pose primeiro) e móveis (pose ao final).
    model_text = re.sub(
        r'(?m)^      <pose frame=\'\'>[^<]*</pose>',
        f'      <pose>{new_pose}</pose>',
        model_text, count=1
    )

    # Torna todos os modelos estáticos (paredes e móveis)
    model_text = model_text.replace('<static>1</static>', '<static>true</static>')
    model_text = model_text.replace('<static>0</static>', '<static>true</static>')

    model_text = convert_link_content(model_text)
    model_text = re.sub(r"<link name='([^']+)'>", r'<link name="\1">', model_text)
    model_text = re.sub(r"<collision name='([^']+)'>", r'<collision name="\1">', model_text)
    model_text = re.sub(r"<visual name='([^']+)'>", r'<visual name="\1">', model_text)
    return model_text


def main():
    with open(SRC, 'r') as f:
        lines = f.read().split('\n')

    # Montar texto com apenas as linhas de definição de modelos (excluir state/gui)
    segments = []
    for start, end in MODEL_LINE_RANGES:
        segments.append('\n'.join(lines[start:end]))
    world_models_text = '\n'.join(segments)

    model_pattern = re.compile(
        r"    <model name='([^']+)'>(.*?)\n    </model>", re.DOTALL
    )
    models = model_pattern.findall(world_models_text)
    print(f"Modelos encontrados: {len(models)} — {[m[0] for m in models]}")

    output_parts = [SDF_HEADER]
    for model_name, model_body in models:
        full_model = f"    <model name='{model_name}'>{model_body}\n    </model>"
        output_parts.append(convert_model(model_name, full_model))
        output_parts.append('\n')
    output_parts.append(SDF_FOOTER)

    final = '\n'.join(output_parts)
    final = re.sub(r" frame=''", '', final)
    final = re.sub(r' frame=""', '', final)
    final = re.sub(r'\n{3,}', '\n\n', final)

    with open(DST, 'w') as f:
        f.write(final)

    model_count = len(re.findall(r'<model name=', final))
    print(f"Modelos no arquivo gerado: {model_count} (incluindo ground_plane)")
    print(f"Arquivo escrito em: {DST}")

    # Verificação de sanidade
    checks = [
        '<static>1</static>', '<static>0</static>', "<static>false</static>",
        "frame=''", '<self_collide>', '<kinematic>',
        '<max_contacts>', '<bounce>', '<torsional>', 'Gazebo/Grey',
        'gazebo.material', '<real_time_update_rate>', '<spherical_coordinates>',
        '<state world_name', '<gui ',
        '<inertial>', '<laser_retro>', '<allow_auto_disable>',
        '<lighting>', '<bullet>',
    ]
    print("\nVerificação de resíduos Classic:")
    for check in checks:
        count = final.count(check)
        status = f"AVISO: {count}x encontrado!" if count > 0 else "OK"
        print(f"  {status:40s} '{check}'")


if __name__ == '__main__':
    main()
