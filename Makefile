# NI2R - ni2r_ros
# SPDX-License-Identifier: BSD 3-Clause "New" or "Revised" License

#
# MARK: - Constants
#

CURRENT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
CATKIN_SRC_DIR := $(CURRENT_DIR)/..

#
# MARK: - Arguments
#

MATCH_LAUNCHER := Main.launch

#
# MARK: - Dependencies names
#

ARUCO_DIR      := $(CATKIN_SRC_DIR)/fiducials
VISION_MSG_DIR := $(CATKIN_SRC_DIR)/vision_msgs
RPLIDAR_DIR    := $(CATKIN_SRC_DIR)/rplidar_ros

#
# MARK: - Run program
#

all:
	@echo "🤖 Run match program 🏁"
	@roslaunch ni2r_ros $(MATCH_LAUNCHER)

#
# MARK: - Utils
#

compile_hard:
	@$(MAKE) rm_build
	@$(MAKE) compile

compile:
	@cd $(CATKIN_SRC_DIR)/.. && catkin_make

rm_build:
	@echo "🗑️ Cleaning up build directories 🏗️"
	@cd $(CATKIN_SRC_DIR)/.. && rm -rf build && rm -rf devel

#
# MARK: - ROS utils
#

install_ros_dependencies:
	# @sudo rosdep init
	@rosdep update
	@rosdep install --from-paths $(CATKIN_SRC_DIR) --ignore-src -r -y

#
# MARK: - Dependencies setup
#

setup_dependencies:
	@echo ""
	@echo "🧬 Setup dependencies for ni2r_ros 📦"
	# @$(MAKE) clone_aruco_package
	@$(MAKE) clone_rplidar_package
	# @$(MAKE) install_ros_dependencies
	@$(MAKE) compile_hard

clone_aruco_package:
	@echo "🧬 Cloning aruco package 📦"
	@rm -rf $(ARUCO_DIR)
	@git clone --single-branch https://github.com/UbiquityRobotics/fiducials $(ARUCO_DIR)
	@cd $(ARUCO_DIR) && git reset --hard 96b329a
	# Update camera, image and dictonary in aruco_detect and fiducial_slam's arguments
	@$(MAKE) clone_vision_msgs_package

clone_vision_msgs_package:
	@echo "🧬 Cloning vision_msgs package 📦"
	@rm -rf $(VISION_MSG_DIR)
	@git clone --depth=1 --branch=melodic-devel https://github.com/ros-perception/vision_msgs $(VISION_MSG_DIR)

clone_rplidar_package:
	@echo "🧬 Cloning rplidar package 📦"
	@rm -rf $(RPLIDAR_DIR)
	@git clone --single-branch https://github.com/Slamtec/rplidar_ros $(RPLIDAR_DIR)
	@cd $(RPLIDAR_DIR) && git reset --hard 4f899e6
