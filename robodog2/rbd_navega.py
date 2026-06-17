# rbd_navega.py — Nó principal do robodog2
#
# Inicializa a casa, as tarefas e o robô; lança o loop autônomo de patrulha
# em thread separada enquanto o MultiThreadedExecutor processa callbacks ROS2.
#
# Uso:
#   alias rbd2_navega='ros2 run robodog2 rbd_navega'

import threading

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import LaserScan

from .rbd_funcoes import scan_retorno, set_node
from .rbd_md import CASA, TAREFAS, ROBO
from .rbd_tabelas import (CM, PD, RT, PC, PT,
                          Tarefas, Tarefas_Ativas, Pesos_Tarefas,
                          Incrementa_Peso, Decrementa_Peso)


class RbdNavega(Node):
    def __init__(self):
        super().__init__('rbd_navega')
        self.create_subscription(LaserScan, '/scan', scan_retorno, 10)

        casa = CASA(
            comodos=CM, posicoes_destino=PD, rotas=RT,
            rotas_centrais=PC, pontos_troca=PT
        )
        tarefas = TAREFAS(
            existentes=list(Tarefas),
            ativas=list(Tarefas_Ativas),
            pesos=list(Pesos_Tarefas),
            incrementos=list(Incrementa_Peso),
            decrementos=list(Decrementa_Peso),
            casa=casa
        )
        self._robo = ROBO(casa=casa, tarefas=tarefas)
        self.get_logger().info('robodog2 pronto')


def main(args=None):
    rclpy.init(args=args)
    node = RbdNavega()

    # set_node antes de iniciar o loop — move_to_goal precisa de _node
    set_node(node)

    # loop de comportamento em thread separada; executor fica livre para
    # processar callbacks do Nav2 action e do laser scan
    behavior_thread = threading.Thread(
        target=node._robo.escolhe_tarefas, daemon=True
    )
    behavior_thread.start()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
