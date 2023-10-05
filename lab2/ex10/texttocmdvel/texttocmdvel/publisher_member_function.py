# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import geometry_msgs.msg


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.subscription_ = self.create_subscription(String, "cmd_text", self.callback, 1)
        self.publisher_ = self.create_publisher(geometry_msgs.msg.Twist, 'turtle1/cmd_vel', 1)
        self.get_logger().info("Succesfully create node")

    def callback(self, msg: String):
        self.get_logger().info("Get message from cmd_text: %s" % msg.data)
        string_msg = msg.data
        turtle_msg = geometry_msgs.msg.Twist()
        if string_msg == "turn_right":
            turtle_msg.angular.z = -1.5
        elif string_msg == "turn_left":
            turtle_msg.angular.z = 1.5
        elif string_msg == "move_forward":
            turtle_msg.linear.x = 1.0
        elif string_msg == "move_backward":
            turtle_msg.linear.x = -1.0

        self.publisher_.publish(turtle_msg)
        self.get_logger().info(f'Publishing: "{turtle_msg.angular.z}" "{turtle_msg.linear.x}" ')


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
