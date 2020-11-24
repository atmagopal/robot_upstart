import robot_upstart

rosip_interface = 'wlp0s20f3'
log_dir = "/home/atmaraaj/hrg/service_log/" # Common log directory for all services
master = "http://172.30.1.155:11311"

roscore_service_name = "my_roscore"

# http://docs.ros.org/en/melodic/api/robot_upstart/html/jobs.html
""" 
name (str) - Name of job to create. Defaults to “ros”, but you might
prefer to use the name of your platform.

interface (str) - Network interface to bring ROS up with. If specified,
the job will come up with that network interface, and ROS_IP will be set
to that interface’s IP address. If unspecified, the job will come up
on system startup, and ROS_HOSTNAME will be set to the system’s hostname.

user (str) - Unprivileged user to launch the job as. Defaults to the user
creating the job.

workspace_setup (str) - Location of the workspace setup file to source for
the job’s ROS context. Defaults to the current workspace.

rosdistro (str) - rosdistro to use for the /etc/ros/DISTRO path. Defaults
to $ROS_DISTRO from the current environment.

master_uri (str) - For systems with multiple computers, you may want this
job to launch with ROS_MASTER_URI pointing to another machine.

log_path (str) - The location to set ROS_LOG_DIR to. If changed from the
default of using /tmp, it is the user’s responsibility to manage log
rotation. 

master_service (str) - Optional: Specify the name of the service that should 
start roscore, preferably one that will be persistent. When specified, other
services that launch nodes/params will activate only after the master service
"""

# CORE ---------------------------------------------------------------# 
j = robot_upstart.Job(name=roscore_service_name) # service name       

j.interface = rosip_interface
j.symlink   = True
j.log_path    = log_dir
j.master_uri = master

# j.user = 'atmaraaj'

# j.workspace_setup ="../setup.bash"

j.add(package="mira_description", filename="launch/display.launch")

# j.install()

# NODES ---------------------------------------------------------------# 
#! Camera
j = robot_upstart.Job(name="ros_camera") # service name       

j.interface = rosip_interface
j.symlink   = True
j.log_path    = log_dir
# j.master_service = roscore_service_name + ".service"
# j.user = 'atmaraaj'


j.roslaunch_wait = True
j.master_uri = master
# j.workspace_setup ="../setup.bash"

j.add(package="realsense2_camera", filename="launch/rs_camera.launch")

j.install()

#! Something else
j = robot_upstart.Job(name="ros_dummy") # service name       

j.interface = rosip_interface
j.symlink   = True
j.log_path    = log_dir
# j.master_service = roscore_service_name + ".service"

j.roslaunch_wait = True
j.master_uri = master
# j.workspace_setup ="../setup.bash"

j.add(package="mira_description", filename="launch/dummy.launch")

j.install()