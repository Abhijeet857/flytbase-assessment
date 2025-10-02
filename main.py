from data_models import Waypoint3D, Mission
from conflict_detector import find_conflict
from visualization import animate_missions
primary_mission = Mission(
    id="primary",
    waypoints=[
        Waypoint3D(x=0, y=50, z=20),
        Waypoint3D(x=100, y=50, z=20)
    ],
    timestamps=[0.0, 10.0]
)

intruder_mission = Mission(
    id="intruder",
    waypoints=[
        Waypoint3D(x=50, y=0, z=10),
        Waypoint3D(x=50, y=100, z=10)
    ],
    timestamps=[0.0, 10.0]
)

conflict_info = find_conflict(primary_mission, intruder_mission, safety_buffer=5.0)

if conflict_info is not None:
    t = conflict_info["time"]
    pos1 = conflict_info["position1"]
    pos2 = conflict_info["position2"]
    print(
        f"Conflict Detected at T={t:.2f}s! "
        f"Drone 1 at ({pos1.x:.2f}, {pos1.y:.2f}, {pos1.z:.2f}), "
        f"Drone 2 at ({pos2.x:.2f}, {pos2.y:.2f}, {pos2.z:.2f})"
    )
else:
    print("No conflict detected.")

#plot_missions([primary_mission, intruder_mission], conflict_info)
animate_missions([primary_mission, intruder_mission])
