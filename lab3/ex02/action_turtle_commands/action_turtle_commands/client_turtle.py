import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtle_action.action import ExecuteTurtleCommand


class MessageTurtleActionClient(Node):

    def __init__(self):
        super().__init__('message_turtle_action_client')
        self._action_client = ActionClient(self, ExecuteTurtleCommand, 'messageturtle')
        self.working = False

    def send_goal(self, order):
        goal_msg = ExecuteTurtleCommand.Goal()

        for com, num in order:
            goal_msg.command = com

            if com == "forward":
                goal_msg.s = num
                goal_msg.angle = 0
            else:
                goal_msg.s = 0
                goal_msg.angle = num

            self._action_client.wait_for_server()
            self._send_goal_future = self._action_client.send_goal_async(goal_msg,
                                                                         feedback_callback=self.feedback_callback)
            self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.result))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback))


def main(args=None):
    rclpy.init(args=args)

    action_client = MessageTurtleActionClient()

    action_client.send_goal([["forward", 2], ["turn_right", 90], ["forward", 1]])
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
