import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions

def generate_launch_description():
    # 获取默认的 URDF 路径
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_urdf_path = os.path.join(urdf_package_path, "urdf", "first_robot.urdf")
    default_rviz_config_path =  os.path.join(urdf_package_path, "config", "rviz2.rviz")
    # 声明一个 URDF 参数，方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_urdf_path),description="加载的模型文件路径"
    )

    # 修复路径拼接并转换为参数值对象 当没有使用xacro时候 参数'xacro ' 修改为 'cat '来运行urdf文件
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

    # 定义 joint_state_publisher 节点
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable="joint_state_publisher"
    ) 

    # 定义 rviz2 节点
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable="rviz2",
        arguments=['-d', default_rviz_config_path]
    ) 

    # 返回 Launch 描述
    return launch.LaunchDescription(
        [
            action_declare_arg_mode_path,
            action_robot_state_publisher,
            action_joint_state_publisher,
            action_rviz_node,
        ]
    )
