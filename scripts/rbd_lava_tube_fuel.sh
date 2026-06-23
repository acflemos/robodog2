#!/usr/bin/env bash
# Lança lava_tube_fuel.world (meshes Fuel DARPA SubT).
set -eo pipefail
source /opt/ros/humble/setup.bash
source "${HOME}/ros2_ws/install/setup.bash"
LAUNCH="${HOME}/ros2_ws/install/robodog2/share/robodog2/launch/rbd_lava_tube_fuel_launch.py"
if [[ ! -f "${LAUNCH}" ]]; then
  echo "rbd_lava_tube_fuel: launch não instalado. Execute: rbd2_build_pkg && rbd2_source" >&2
  exit 1
fi
exec ros2 launch robodog2 rbd_lava_tube_fuel_launch.py "$@"