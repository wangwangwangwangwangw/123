import os
import launch
import launch.launch_description_sources
import launch_ros
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions

def generate_launch_description():
    # 获取功能报的share 路径
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_path = os.path.join(urdf_package_path, "urdf", "fishbot/fishbot.urdf.xacro")
    # default_rviz_config_path =  os.path.join(urdf_package_path, "config", "rviz2.rviz")
    default_gazebo_world_path =  os.path.join(urdf_package_path, "world", "custom_room.world")

    
    # 声明一个 xacro参数，方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_xacro_path),description="加载的模型文件路径"
    )

    # 修复路径拼接并转换为参数值对象
    substitutions_commed_result = launch.substitutions.Command(
        ['xacro ', launch.substitutions.LaunchConfiguration('model')]
    )
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_commed_result, value_type=str
    )

    # 定义 robot_state_publisher 节点
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description_value}]
    )

    action_launch_gazebo =launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']
        ),
        launch_arguments=[("world",default_gazebo_world_path),("verbose",'true')]
    )

    action_spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=['-topic','/robot_description','-entity',"fishbot"]
    )
    # 定义 rviz2 节点
    # action_rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable="rviz2",
    #     arguments=['-d', default_rviz_config_path]
    # ) 

    # 返回 Launch 描述
    return launch.LaunchDescription(
        [
            action_declare_arg_mode_path,
            action_robot_state_publisher,
            action_launch_gazebo,
            action_spawn_entity
            # action_rviz_node,
        ]
    )
