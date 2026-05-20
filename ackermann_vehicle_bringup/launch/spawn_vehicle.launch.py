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
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def get_model_property_value(file_name, property_name, marker='value="'):
    with open(file_name, 'r') as fp:
        lines = fp.readlines()
        for row in lines:
            if row.find(property_name) != -1:            
                char_idx1 = row.find(marker) + len(marker)
                char_idx2 = char_idx1 + row[char_idx1: ].find('"')
                return row[char_idx1: char_idx2]
            
def launch_setup(context: LaunchContext, *args, **kwargs):
    # Configure ROS nodes for launch
    # Setup project paths
    pkg_project_gazebo = get_package_share_directory('ackermann_vehicle_gazebo')
    pkg_project_description = get_package_share_directory('ackermann_vehicle_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    # set world filename and vehicle type and name
    world_file = LaunchConfiguration('world_file')
    world_file_path = PathJoinSubstitution([pkg_project_gazebo, 'worlds', world_file])
    vehicle_type = LaunchConfiguration('vehicle_type')
    vehicle_name = LaunchConfiguration('vehicle_name')
    
    # Load SDF and Xacro files
    xacro_file = os.path.join(pkg_project_description, 'models', vehicle_type.perform(context), 'model.sdf.xacro')
    sdf_file  =  PathJoinSubstitution([pkg_project_description, 'models', vehicle_type, 'model.sdf'])
        
    # Spawn Model
    spawn_model = IncludeLaunchDescription(
        os.path.join(pkg_ros_gz_sim, 'launch', 'gz_spawn_model.launch.py'),
        launch_arguments={
            'world': get_model_property_value(world_file_path.perform(context), 'world', 'name="'),
            'file': sdf_file,
            'entity_name': vehicle_name,
            'z': str(float(get_model_property_value(xacro_file, 'tire_radius')) +
                     float(get_model_property_value(xacro_file, 'chassis_height_offset')))
        }.items()
    )
    
    return [spawn_model]
            

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world_file', default_value='obstacleField.sdf'),
        DeclareLaunchArgument('vehicle_type', default_value='slash_4x4_ultimate'),
        DeclareLaunchArgument('vehicle_name', default_value='sputnik'),
        OpaqueFunction(function = launch_setup)
    ])
