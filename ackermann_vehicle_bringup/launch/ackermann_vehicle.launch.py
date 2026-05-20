# Copyright 2022 Open Source Robotics Foundation, Inc.
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

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.descriptions import ParameterValue
from launch_ros.actions import Node

            
def launch_setup(context: LaunchContext, *args, **kwargs):
    # Configure ROS nodes for launch
    # Setup project paths
    pkg_project_bringup = get_package_share_directory('ackermann_vehicle_bringup')
    pkg_project_gazebo = get_package_share_directory('ackermann_vehicle_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    # set world filename and vehicle type and name
    world_file = LaunchConfiguration('world_file')
    world_file_path = PathJoinSubstitution([pkg_project_gazebo, 'worlds', world_file])
    vehicle_type = LaunchConfiguration('vehicle_type')
    vehicle_name = LaunchConfiguration('vehicle_name')
    
    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': world_file_path}.items()
    )
        
    # Spawn Vehicle
    spawn_vehicle = IncludeLaunchDescription(
        os.path.join(pkg_project_bringup, 'launch', 'spawn_vehicle.launch.py'),
        launch_arguments={
            'world_file': world_file,
            'vehicle_type': vehicle_type,
            'vehicle_name': vehicle_name
        }.items()
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_project_bringup, 'config', 'ackermann_vehicle_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local'
        }],
        output='screen'
    ) 
    
    return [
        gz_sim,
        spawn_vehicle,
        bridge,
    ]
            

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world_file', default_value='obstacleField.sdf'),
        DeclareLaunchArgument('vehicle_type', default_value='slash_4x4_ultimate'),
        DeclareLaunchArgument('vehicle_name', default_value='sputnik'),
        OpaqueFunction(function = launch_setup)
    ])
