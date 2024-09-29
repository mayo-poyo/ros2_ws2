import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import sys
class Driver_node(Node):

    def __init__(self):
        super().__init__('driving_custom_Node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription_ = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer_=self.create_timer(0.1,self.the_callback)
        self.pose=None
        self.subscription_

    def pose_callback(self, data):
        self.pose=data
        


    def the_callback(self):
        print(self.pose)
        curr_x = self.pose.x
        curr_y = self.pose.y
        goal=Pose()
        goal.x = float (sys.argv[1])
        goal.y = float (sys.argv[2])
        goal.theta = float (sys.argv[3])
        curr_theta = self.pose.theta
        route_theta = math.atan2((goal.y-curr_y),(goal.x-curr_x))
        dist = math.sqrt((curr_x - goal.x)**2+(curr_y - goal.y )**2)
        dist_tol=0.1
        msg = Twist()
        kp=1.4
        
        
        if abs(curr_theta-route_theta)>0.01 and abs(dist>dist_tol):
            
            msg.linear.x=0.0
            msg.linear.y=0.0
            msg.angular.z=(route_theta-curr_theta)*kp
            print('pointing to goal, rotating '+ str (msg.angular.z))
        else:
            if abs(dist<=dist_tol):
                print('close to goal '+ str (dist))
                msg.linear.x=0.0
                msg.linear.y=0.0
                if(abs(goal.theta - curr_theta)>0.01)and(abs(goal.theta - curr_theta-math.radians(360))>0.01):
                    print('final rotation :' + str(goal.theta - curr_theta))
                    if(goal.theta<curr_theta):
                        print('positive')
                        msg.angular.z= (goal.theta - curr_theta)*kp
                    else:
                        print('negative')
                        print('goal is '+ str (goal.theta)+'current theta :'+ str(curr_theta))
                        msg.angular.z= (goal.theta  -math.radians(360)- curr_theta)
                else:
                    self.get_logger().info('reached!')
                    quit()
                
            else:
                msg.linear.x= dist*kp
                msg.linear.y= 0.0
                msg.angular.z= 0.0
                print('going towards goal')
        
       
        self.publisher_.publish(msg)
        print(msg)
        
        
        # W = v / r

        

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Driver_node()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()