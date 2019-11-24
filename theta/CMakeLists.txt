cmake_minimum_required(VERSION 2.8.3)
project(theta)

find_package(OpenCV REQUIRED)


find_package(catkin REQUIRED COMPONENTS
  roslib
  rospy
  sensor_msgs
  std_msgs
  cv_bridge
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES theta
#  CATKIN_DEPENDS roslib rospy sensor_msgs std_msgs
#  DEPENDS system_lib
)

include_directories(
  /usr/local/include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  )

#add_executable()
#target_link_libraries( ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})
