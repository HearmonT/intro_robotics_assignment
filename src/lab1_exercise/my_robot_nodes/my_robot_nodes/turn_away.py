#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from lab_interfaces.msg import ObstacleInfo
from my_robot_interfaces.msg import RobotStatus  # Our new message!
from std_srvs.srv import SetBool

class TurnAwayNode(Node):
    def __init__(self):
        super().__init__('turn_away')
        
        self.declare_parameter('forward_speed', 0.2)
        self.declare_parameter('turn_speed', 0.5)
        
        # State variable for enabling/disabling movement
        self.is_enabled = False
        
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_publisher = self.create_publisher(RobotStatus, '/robot_status', 10)
        
        self.subscription = self.create_subscription(
            ObstacleInfo,
            '/obstacle',
            self.obstacle_callback,
            10)
        
        # Service server to enable or disable the robot
        self.enable_service = self.create_service(
            SetBool,
            'turn_away_enable',
            self.enable_service_callback)

    def enable_service_callback(self, request, response):
        self.is_enabled = request.data
        response.success = True
        response.message = "Robot enabled state updated."
        self.get_logger().info(f"Robot enabled set to: {self.is_enabled}")
        return response

    def obstacle_callback(self, msg):
        forward_speed = self.get_parameter('forward_speed').value
        turn_speed = self.get_parameter('turn_speed').value
        
        twist = Twist()
        status = RobotStatus()
        status.obstacle_distance = float(msg.distance)
        
        if not self.is_enabled:
            # Robot is stopped when disabled
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            status.state = "stopped"
        elif not msg.too_close:
            twist.linear.x = float(forward_speed)
            twist.angular.z = 0.0
            status.state = "forward"
        else:
            twist.linear.x = 0.0
            status.state = "turning"
            if msg.angle > 0:
                twist.angular.z = -float(turn_speed)
            else:
                twist.angular.z = float(turn_speed)
                
        self.cmd_publisher.publish(twist)
        self.status_publisher.publish(status)

def main(args=None):
    rclpy.init(args=args)
    node = TurnAwayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()