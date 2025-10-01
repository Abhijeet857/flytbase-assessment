from data_models import Waypoint3D, Mission

def get_position_at_time(mission: Mission, time_t: float) -> Waypoint3D:
    waypoints = mission.waypoints
    timestamps = mission.timestamps

    if time_t <= timestamps[0]:
        return waypoints[0]
    if time_t >= timestamps[-1]:
        return waypoints[-1]

    for i in range(len(timestamps) - 1):
        t0 = timestamps[i]
        t1 = timestamps[i + 1]
        if t0 <= time_t <= t1:
            w0 = waypoints[i]
            w1 = waypoints[i + 1]
            if t1 == t0:
                alpha = 0.0
            else:
                alpha = (time_t - t0) / (t1 - t0)
            x = w0.x + alpha * (w1.x - w0.x)
            y = w0.y + alpha * (w1.y - w0.y)
            z = w0.z + alpha * (w1.z - w0.z)
            return Waypoint3D(x=x, y=y, z=z)
    return waypoints[-1]

def calculate_distance(p1: Waypoint3D, p2: Waypoint3D) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2) ** 0.5

def find_conflict(mission1: Mission, mission2: Mission, safety_buffer: float):
    """
    Simulates two missions and checks for spatiotemporal conflicts.

    Args:
        mission1: The first mission object.
        mission2: The second mission object.
        safety_buffer: The minimum allowed distance between drones.

    Returns:
        A dictionary with conflict info if a conflict is found, otherwise None.
    """
    # Iterate through time at a fixed step
    time = 0.0
    end_time = max(mission1.timestamps[-1], mission2.timestamps[-1])
    step = 0.5
    while time <= end_time + 1e-6:  # small epsilon to include 10.0
        pos1 = get_position_at_time(mission1, time)
        pos2 = get_position_at_time(mission2, time)
        distance = calculate_distance(pos1, pos2)
        if distance < safety_buffer:
            return {
                "time": time,
                "position1": pos1,
                "position2": pos2
            }
        time += step
    return None
