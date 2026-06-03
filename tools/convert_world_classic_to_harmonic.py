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
  cma_moveis.world — a converter (ver TODO abaixo)
"""

import re

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — editar para cada conversão
# ---------------------------------------------------------------------------

SRC = '/home/antonio/ros2_ws/src/robodog2/worlds/robodog1_classic/cma_vazio.world'
DST = '/home/antonio/ros2_ws/src/robodog2/worlds/cma_vazio.world'

# Poses corretas extraídas do bloco <state> do arquivo Classic
# Para obter: grep -A3 '<model name=' <arquivo.world> (dentro do bloco <state>)
STATE_POSES = {
    "ground_plane":   "0 0 0 0 0 0",
    "cma_escritorio": "-1.79682 1.02121 0 0 0 0",
    "cma_L2":         "4.51683 -3.24587 0 0 0 0",
    "cma_L3":         "6.37221 -2.26022 0 0 0 0",
    "cma_L5":         "3.77502 1.45512 0 0 0 0",
    "cma_U":          "4.97895 -9.92408 0 0 0 0",
    "cma_area2":      "4.52275 5.67862 0 0 0 0",
    "cma_banheiro":   "-5.22928 3.4871 0 0 0 0",
    "cma_banheiro_e": "1.18358 3.89879 0 0 0 0",
    "cma_dispensa":   "2.52584 4.40119 0 0 0 0",
    "cma_lavabo":     "7.72297 -4.09302 0 0 0 0",
    "cma_parede_L":   "4.97628 -6.69992 0 0 0 0",
    "cma_parede_t":   "0.164039 -3.24829 0 0 0 0",
    "cma_qe":         "1.79561 6.31228 0 0 0 0",
    "cma_quartos":    "-2.58169 -7.26456 0 0 0 0",
    "cma_varanda1":   "-6.32518 -2.59313 0 0 0 0",
}

# Intervalo de linhas (0-indexed) com definições de modelos no arquivo Classic.
# Excluir: bloco <state>, bloco <gui>, ground_plane original.
# Para cma_vazio.world: state=linhas 548-1016, gui=1017-1023
# world models: [82:548] + [1024:fim]
# Ajustar estes offsets para outros arquivos .world
MODEL_LINE_RANGES = [
    (82, 548),     # cma_escritorio
    (1024, None),  # todos os outros (até o fim, excluindo </world></sdf>)
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
    text = re.sub(r'\s*<self_collide>0</self_collide>', '', text)
    text = re.sub(r'\s*<kinematic>0</kinematic>', '', text)
    text = re.sub(r'\s*<gravity>1</gravity>', '', text)
    text = re.sub(r'\s*<max_contacts>\d+</max_contacts>', '', text)
    text = re.sub(r'\s*<contact>\s*<ode/>\s*</contact>', '', text)
    text = re.sub(r'\s*<bounce/>', '', text)
    text = re.sub(r'\s*<torsional>\s*<ode/>\s*</torsional>', '', text)
    text = re.sub(r'\s*<ode/>', '', text)
    text = re.sub(
        r'<material>\s*<script>.*?</script>\s*<ambient>.*?</ambient>\s*</material>',
        '<material>\n            <ambient>0.7 0.7 0.7 1</ambient>\n'
        '            <diffuse>0.7 0.7 0.7 1</diffuse>\n          </material>',
        text, flags=re.DOTALL
    )
    text = re.sub(r"<pose frame=''>(.*?)</pose>", r'<pose>\1</pose>', text)
    text = re.sub(r'\b-0\b', '0', text)
    text = re.sub(r'\s*<friction>\s*</friction>', '', text)
    text = re.sub(r'\s*<surface>\s*</surface>', '', text)
    return text


def convert_model(model_name, model_text):
    new_pose = STATE_POSES.get(model_name, "0 0 0 0 0 0")
    model_text = re.sub(r"<model name='([^']+)'>", r'<model name="\1">', model_text)
    model_text = re.sub(
        r"<pose frame=''>[^<]*</pose>",
        f'<pose>{new_pose}</pose>',
        model_text, count=1
    )
    model_text = model_text.replace('<static>1</static>', '<static>true</static>')
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
        '<static>1</static>', "frame=''", '<self_collide>', '<kinematic>',
        '<max_contacts>', '<bounce/>', '<torsional>', 'Gazebo/Grey',
        'gazebo.material', '<real_time_update_rate>', '<spherical_coordinates>',
        '<state world_name', '<gui ',
    ]
    print("\nVerificação de resíduos Classic:")
    for check in checks:
        count = final.count(check)
        status = f"AVISO: {count}x encontrado!" if count > 0 else "OK"
        print(f"  {status:30s} '{check}'")


if __name__ == '__main__':
    main()
