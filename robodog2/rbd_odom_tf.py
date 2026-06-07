#!/usr/bin/env python3
# rbd_odom_tf.py
# ==============
# Publica o TF odom→base_footprint a partir da mensagem /odom.
#
# O bridge ros_gz_bridge não converte correctamente o TF do OdometryPublisher
# do Gazebo Harmonic para tf2_msgs/TFMessage. A solução standard para Gazebo
# Harmonic + Nav2 é ler a mensagem /odom (que IS bridged) e re-publicar o
# transform odom→base_footprint via TransformBroadcaster.
#
# Sem este nó:  TF tree = (map→odom) DESLIGADO de (base_footprint→base_link→...)
# Com este nó:  TF tree = map→odom→base_footprint→base_link→{rodas,laser_link,...}
#
# Usado em:
#   rbd_gz_x3_launch.py  (lançado junto com o Gazebo e o bridge)

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

# ros_gz_bridge publica /odom com BEST_EFFORT (sensor data profile).
# Usar RELIABLE causaria mismatch silencioso — a callback nunca seria chamada.
_SENSOR_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
)


class OdomTfBroadcaster(Node):

    def __init__(self):
        super().__init__('odom_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.create_subscription(Odometry, '/odom', self._odom_cb, _SENSOR_QOS)
        self.get_logger().info('odom_tf_broadcaster: publicando odom→base_footprint')

    def _odom_cb(self, msg: Odometry):
        t = TransformStamped()
        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomTfBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
