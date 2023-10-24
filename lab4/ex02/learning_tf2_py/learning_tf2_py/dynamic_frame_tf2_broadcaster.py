import math

import numpy as np
from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


class DynamicFrameBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.declare_parameter('radius', 2)
        self.declare_parameter('direction_of_rotation', 1)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        self.theta = np.linspace(0, 2 * np.pi, num=1000)
        self.point_index = 0

    def broadcast_timer_callback(self):
        radius = self.get_parameter('radius').get_parameter_value().integer_value
        direction_of_rotation = self.get_parameter('direction_of_rotation').get_parameter_value().integer_value
        self.point_index %= self.theta.shape[0]
        self.point_index += 1
        self.get_logger().info(f'{self.theta.shape[0]}')
        self.get_logger().info(f"{self.point_index}")
        if (abs(direction_of_rotation) != 1):
            self.get_logger().info('Direction of rotation must be 1 or -1')
            quit()
        x = radius * np.sin(self.theta[self.point_index - 1])
        y = radius * np.cos(self.theta[self.point_index - 1])
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'turtle1'
        t.child_frame_id = 'carrot1'
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = float(direction_of_rotation)

        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
