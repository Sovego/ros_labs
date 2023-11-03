import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math


class SinusoidalMotion(Node):
    def __init__(self):
        super().__init__('sinusoidal_motion')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        twist_msg = Twist()
        twist_msg.linear.x = math.sin(self.counter)  # Set linear velocity to sin(counter)
        twist_msg.angular.z = 0.5  # Set angular velocity to a constant value (e.g., 0.5 rad/s)
        self.publisher.publish(twist_msg)
        self.counter += 0.1  # Increment the counter for the next iteration


def main(args=None):
    rclpy.init(args=args)
    node = SinusoidalMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
