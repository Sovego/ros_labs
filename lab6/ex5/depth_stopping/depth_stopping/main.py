#!/usr/bin/env pythonм
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge,CvBridgeError
import cv2
import numpy as np    
class Turtle(Node):
    def __init__(self):
        super().__init__('depth_stopping_Node')
        self.publisher_ = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Image, '/depth/image', self.pose_callback, 1)
        self.timer = self.create_timer(0.2, self.go_forward)
        self.msg = None

    def pose_callback(self, data):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(data,desired_encoding="passthrough")
        self.msg = img

    def go_forward(self):
        message = Twist()
        image = self.msg
        height, width = image.shape
        if width!=0:
            center_x, center_y = width // 2, height // 2
            num_points = 10
            points = []
            for i in range(num_points):
                angle = 2 * np.pi * i / num_points
                x = int(center_x + 0.8 * center_x * np.cos(angle))
                y = int(center_y + 0.8 * center_y * np.sin(angle))
                points.append((x, y))
            average_point = (int(np.mean([point[0] for point in points])), int(np.mean([point[1] for point in points])))
            pixel_values = [image[point[1], point[0]] for point in points]
            average_pixel_value = np.mean(pixel_values, axis=0)
            #center_color = image[int(self.msg.width*self.msg.height/2+self.msg.width/2)]
            self.get_logger().info('dist {0} '.format(average_pixel_value))

            message.linear.x = 0.0 if (average_pixel_value<=1.0) else 0.1
            message.angular.z = 0.0
            self.publisher_.publish(message)    

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Turtle()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
