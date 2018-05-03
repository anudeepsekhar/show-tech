import rospy
import math
from geometry_msgs.msg import Point,Twist
from nav_msgs.msg import Odometry
from rosgraph_msgs.msg import Clock
from tf.transformations import euler_from_quaternion


def getOdom(msg):
	global x, y, z
	global roll, pitch ,yaw 
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y
	z = msg.pose.pose.position.z
	q = msg.pose.pose.orientation
	qs = [q.x,q.y,q.z,q.w]
	(roll,pitch, yaw) = euler_from_quaternion(qs)

def isTarget(goalx,goaly):

	if(abs(goalx-x)<0.1):
		if(abs(goaly - y) < 0.1):
			print("target reached..!!")
			return True
		else:
			return False
	else:
		return False		


def move(goalx,goaly):
	
	goal.x = goalx
	goal.y = goaly
	
	err_x = goal.x - x
	err_y = goal.y - y

	angle_to_goal = math.atan2(err_y,err_x)

	print("target:"+str(math.degrees(angle_to_goal)))
	print ("angle:"+str(math.degrees(yaw)))
	
	err_a = angle_to_goal - yaw
	print("diff:"+str(math.degrees(err_a)))
	# if(abs(err_a)>math.pi/2 or abs(err_a)<math.pi):
	# 	err_a = err_a-math.pi
	if abs(err_a) > 0.1:
		linearx = 0.0
		angularz = 0.3 * (err_a/abs(err_a))
		if(abs(err_a)>math.radians(350)):
			angularz = -1* angularz
	else:
		linearx = 0.5
		angularz = 0.0

	print("v:"+str(angularz))

	return linearx,angularz

def update_target(x,y):
	goal.x = x
	goal.y = y
	print("x:"+str(x)+" y:"+str(y))


def main2():
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
	rospy.Subscriber('/odom',Odometry, getOdom)
	rospy.init_node('talker', anonymous = True)
	msg = Twist()
	rate = rospy.Rate(10)
	i = 0

	while not rospy.is_shutdown():

		
		reached = isTarget(goal.x,goal.y)
		# print(reached)
		targets = [[0,0],[5,0],[5,5],[0,5],[0,0]]
		target = targets[i]		
		# print target
		reached = isTarget(goal.x,goal.y)
		if(reached):
			update_target(target[0],target[1])
			if(i>=len(targets)- 1):
				i = 0
			else:
				i = i+1

		v_x,a_z = move(goal.x,goal.y)



		msg.linear.x = v_x
		msg.angular.z = a_z


	
	
		pub.publish(msg)
		rate.sleep()



if __name__ == '__main__':
	goal = Point ()
	# target = Point ()
	


	main2()