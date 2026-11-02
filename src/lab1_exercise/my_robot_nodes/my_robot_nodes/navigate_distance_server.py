#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Twist
from my_robot_interfaces.action import NavigateDistance

class NavigateDistanceServer(Node):
    def __init__(self):
        super().__init__('navigate_distance_server')
        
        self._action_server = ActionServer(
            self,
            NavigateDistance,
            'navigate_distance',
            self.execute_callback)
            
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Navigate Distance Action Server has been started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'Executing goal: drive {goal_handle.request.target_distance} meters at {goal_handle.request.speed} m/s')
        
        feedback_msg = NavigateDistance.Feedback()
        result = NavigateDistance.Result()
        
        target_distance = goal_handle.request.target_distance
        speed = goal_handle.request.speed
        
        # Simple simulation: assume constant speed and estimate distance over time
        current_distance = 0.0
        r = self.create_rate(10) # 10 Hz loop
        
        twist = Twist()
        twist.linear.x = float(speed)
        
        while current_distance < target_distance:
            # Check if client canceled the goal
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                twist.linear.x = 0.0
                self.cmd_publisher.publish(twist)
                self.get_logger().info('Goal canceled!')
                result.total_distance_traveled = current_distance
                result.success = False
                return result
                
            # Publish movement command
            self.cmd_publisher.publish(twist)
            
            # Increment simulated distance (speed * time_delta)
            current_distance += speed * 0.1
            if current_distance > target_distance:
                current_distance = target_distance
                
            feedback_msg.current_distance_traveled = current_distance
            goal_handle.publish_feedback(feedback_msg)
            
            r.sleep()
            
        # Stop the robot when finished
        twist.linear.x = 0.0
        self.cmd_publisher.publish(twist)
        
        goal_handle.succeed()
        result.total_distance_traveled = current_distance
        result.success = True
        
        self.get_logger().info('Goal succeeded!')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavigateDistanceServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()