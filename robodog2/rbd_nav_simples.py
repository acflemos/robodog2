#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rbd_nav_simples.py — teste de navegação com BasicNavigator (API oficial Nav2)
#
# Objectivo: isolar se o problema está no código de envio de goals (rbd_funcoes.py)
# ou na configuração DWB/costmap.
#
# Uso (com rbd2_simulador_x3 a correr):
#   ros2 run robodog2 rbd_nav_simples
#   ros2 run robodog2 rbd_nav_simples --ros-args -p goal_x:=-2.0 -p goal_y:=-2.5

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration


def main():
    rclpy.init()
    nav = BasicNavigator()

    nav.get_logger().info('Esperando Nav2 activo...')
    nav.waitUntilNav2Active()
    nav.get_logger().info('Nav2 activo. Enviando goal.')

    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.header.stamp = nav.get_clock().now().to_msg()
    goal.pose.position.x = -2.0
    goal.pose.position.y = -2.5
    goal.pose.position.z = 0.0
    goal.pose.orientation.x = 0.0
    goal.pose.orientation.y = 0.0
    goal.pose.orientation.z = 0.0
    goal.pose.orientation.w = 1.0

    nav.get_logger().info(f'Goal: ({goal.pose.position.x}, {goal.pose.position.y})')
    nav.goToPose(goal)

    i = 0
    while not nav.isTaskComplete():
        i += 1
        feedback = nav.getFeedback()
        if feedback and i % 10 == 0:
            etr = Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            nav.get_logger().info(f'ETR: {etr:.1f}s')
        if i > 600:
            nav.get_logger().warn('Timeout (60s) — cancelando')
            nav.cancelTask()
            break

    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        nav.get_logger().info('CHEGUEI! :-)')
    elif result == TaskResult.CANCELED:
        nav.get_logger().warn('Goal cancelado')
    else:
        nav.get_logger().warn(f'Falhou — resultado: {result}')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
