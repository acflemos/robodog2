#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# rbd_funcoes.py — Funções de navegação, leitura de laser e gestão de pesos
#
# Portado do robodog1 (ROS1) para ROS2 Humble.
# Principais mudanças:
#   - rospy/actionlib/MoveBase → rclpy/ActionClient/NavigateToPose (Nav2)
#   - move_to_goal() usa threading.Event para bloquear o loop de comportamento
#     enquanto o executor ROS2 processa os callbacks da action (sem deadlock)
#   - _node/_nav_client: referência ao nó Node, definida por set_node() em rbd_navega
# =============================================================================

import math
import threading
import time

import rclpy
from rclpy.action import ActionClient
from sensor_msgs.msg import LaserScan
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import Quaternion, Twist

from .rbd_tabelas import (PD, CM, RT, PC, PT,
                          Tarefas_Ativas, Pesos_Tarefas, Decrementa_Peso)


# =============================================================================
# Referência ao nó ROS2 — definida por set_node() chamado em rbd_navega.py
# =============================================================================
_node = None
_nav_client = None
_cmd_vel_pub = None

DIST_PAREDE_MIN = 0.35  # distância mínima a parede para navegação segura (metros)


def set_node(node):
    global _node, _nav_client, _cmd_vel_pub
    _node = node
    _nav_client = ActionClient(node, NavigateToPose, 'navigate_to_pose')
    _cmd_vel_pub = node.create_publisher(Twist, '/cmd_vel', 10)


# =============================================================================
# Variáveis globais de estado
# =============================================================================

# Leituras do laser nas 4 direções: [Frente, Trás, Direita, Esquerda]
m  = [0, 0, 0, 0]
m1 = m  # mesma referência (não é cópia)

lc = [0, 0, 0, 0]
dc = [0, 0, 0, 0]

p1 = PD[0]
p2 = PD[42]

CX = [0, 0, 0, 0]
CY = [0, 0, 0, 0]

f  = 0.6  # folga em relação à parede (metros)
ls = 3.5  # alcance máximo do LiDAR (metros) — ajustar para o sensor do ROSMaster X3

# Goal global reutilizado em move_to_goal(); orientação preenchida por direciona()
goal = NavigateToPose.Goal()


# =============================================================================
# Funções de leitura do laser scan
# =============================================================================

def scan_retorno(scan_data):
    global m
    F = average_between_indices(scan_data.ranges, 0, 5)
    if math.isinf(F):
        F = ls
    T = average_between_indices(scan_data.ranges, 180, 185)
    if math.isinf(T):
        T = ls
    D = average_between_indices(scan_data.ranges, 270, 275)
    if math.isinf(D):
        D = ls
    E = average_between_indices(scan_data.ranges, 90, 95)
    if math.isinf(E):
        E = ls
    m = [F, T, D, E]


def average_between_indices(ranges, i, j):
    valid = [x for x in ranges[i:j+1] if not math.isnan(x)]
    if not valid:
        return ls
    return sum(valid) / float(len(valid))


# =============================================================================
# Recuperação de proximidade a paredes
# =============================================================================

def foge_de_parede():
    """Recua e roda para ganhar espaço quando preso junto a uma parede.

    Chamada automaticamente no início de move_to_goal(). Usa leituras do laser
    em m = [Frente, Trás, Direita, Esquerda] para decidir a direção de escape.
    Publica directamente em /cmd_vel (Nav2 está idle após goal falhado).
    Tenta até 2 vezes se ainda estiver perto após a primeira manobra.
    """
    global m, _cmd_vel_pub, _node
    if _cmd_vel_pub is None:
        return
    if min(m) == 0:      # laser ainda não recebido (arranque)
        return

    for tentativa in range(2):
        if min(m) >= DIST_PAREDE_MIN:
            return       # espaço suficiente — nada a fazer

        F, T, D, E = m[0], m[1], m[2], m[3]
        _node.get_logger().info(
            f'Parede próxima (F={F:.2f} T={T:.2f} D={D:.2f} E={E:.2f})'
            f' — tentativa {tentativa + 1}'
        )

        twist = Twist()
        # escapar para o lado com mais espaço livre
        if T >= F:
            twist.linear.x = -0.15   # mais livre atrás → recua
        else:
            twist.linear.x = 0.15    # mais livre à frente → avança

        for _ in range(25):           # 2.5 s (~0.38 m de translação)
            _cmd_vel_pub.publish(twist)
            time.sleep(0.1)

        # roda ~170° para sair do alinhamento com o canto
        rot = Twist()
        rot.angular.z = 1.0
        for _ in range(30):           # 3.0 s (~170°)
            _cmd_vel_pub.publish(rot)
            time.sleep(0.1)

        _cmd_vel_pub.publish(Twist())  # para
        time.sleep(1.0)               # aguarda costmap actualizar com nova scan


# =============================================================================
# Navegação via Nav2 (NavigateToPose action)
# =============================================================================

def move_to_goal(xGoal, yGoal):
    # -------------------------------------------------------------------------
    # Envia um goal ao Nav2 e bloqueia até receber resultado (máx 60 s).
    # A orientação final deve estar em goal.pose.pose.orientation antes desta
    # chamada — preenchida por TAREFAS.direciona() em rbd_md.py.
    #
    # Usa threading.Event para esperar o resultado sem chamar spin_until_future,
    # que causaria deadlock com o MultiThreadedExecutor ativo em rbd_navega.py.
    # ==========================================================================
    global goal, _node, _nav_client

    foge_de_parede()   # escapa de cantos/paredes antes de enviar goal ao Nav2

    goal_msg = NavigateToPose.Goal()
    goal_msg.pose.header.frame_id = 'map'
    goal_msg.pose.header.stamp = _node.get_clock().now().to_msg()
    goal_msg.pose.pose.position.x = float(xGoal)
    goal_msg.pose.pose.position.y = float(yGoal)
    goal_msg.pose.pose.position.z = 0.0
    goal_msg.pose.pose.orientation = goal.pose.pose.orientation

    while not _nav_client.wait_for_server(timeout_sec=5.0):
        _node.get_logger().info('Esperando navigate_to_pose...')

    done_event = threading.Event()
    result_holder = [None]

    def goal_response_cb(future):
        gh = future.result()
        if not gh.accepted:
            _node.get_logger().warn('Goal rejeitado pelo Nav2')
            result_holder[0] = False
            done_event.set()
            return
        gh.get_result_async().add_done_callback(result_cb)

    def result_cb(future):
        status = future.result().status
        result_holder[0] = (status == GoalStatus.STATUS_SUCCEEDED)
        done_event.set()

    _nav_client.send_goal_async(goal_msg).add_done_callback(goal_response_cb)

    if not done_event.wait(timeout=60.0):
        _node.get_logger().warn('Timeout ao aguardar navegação')
        return False

    if result_holder[0]:
        _node.get_logger().info('CHEGUEI! :-)')
    else:
        _node.get_logger().info('Nao consegui chegar :-/')
    return bool(result_holder[0])


# =============================================================================
# Mapeamento experimental por quadrado (legacy — não integrado ao loop principal)
# =============================================================================

def calcula_quadrado(posicao_inicial, medidas_inicial_scanner):
    global CX, CY, f
    pi = posicao_inicial
    ms = medidas_inicial_scanner
    CX[0] = pi[0] - ms[1] + f
    CY[0] = pi[1] - ms[2] + f
    CX[1] = pi[0] + ms[0] - f
    CY[1] = pi[1] - ms[2] + f
    CX[2] = pi[0] + ms[0] - f
    CY[2] = pi[1] + ms[3] - f
    CX[3] = pi[0] - ms[1] + f
    CY[3] = pi[1] + ms[3] - f
    lc_local = [CX[1]+f, CY[1]-f, CX[3]-f, CY[3]+f]
    comprimento = abs(lc_local[3] - lc_local[1])
    largura     = abs(lc_local[2] - lc_local[0])
    print('limites lc =', lc_local, 'comp =', comprimento, 'larg =', largura)


def quadrado(posicao_inicial):
    global m, f, ls, m1, CX, CY
    pi = posicao_inicial
    m1 = m
    calcula_quadrado(pi, m1)
    for ix in range(4):
        move_to_goal(CX[ix], CY[ix])


# =============================================================================
# Gestão de pesos de tarefas (versão standalone com variáveis globais)
#
# NOTA: estas funções operam sobre as variáveis globais importadas de rbd_tabelas
# e NÃO são chamadas no fluxo principal do loop — o loop usa métodos de TAREFAS
# (rbd_md.py) que operam sobre self.pesos_tarefas. Mantidas para compatibilidade.
# =============================================================================

def decrementa_peso_tarefa(tarefa_concluida):
    global Tarefas_Ativas, Pesos_Tarefas, Decrementa_Peso
    itc = Tarefas_Ativas.index(tarefa_concluida)
    Pesos_Tarefas[itc] = Decrementa_Peso[itc]


def verifica_pesos_negativos():
    global Pesos_Tarefas, Tarefas_Ativas
    nta = len(Tarefas_Ativas)
    total_negativos = sum(1 for p in Pesos_Tarefas if p <= 0)
    if total_negativos >= nta:
        peso_minimo = min(Pesos_Tarefas)
        incrementador = peso_minimo * -1 + 1
        for i in range(nta):
            Pesos_Tarefas[i] += incrementador


def prioriza_tarefas():
    global Tarefas_Ativas, Pesos_Tarefas
    verifica_pesos_negativos()
    lista = []
    for i, tarefa in enumerate(Tarefas_Ativas):
        peso = Pesos_Tarefas[i]
        if peso > 0:
            lista.extend([tarefa] * peso)
    return lista
