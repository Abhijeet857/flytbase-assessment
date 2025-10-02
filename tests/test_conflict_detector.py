import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from data_models import Waypoint3D, Mission
from conflict_detector import find_conflict
from conflict_detector import get_position_at_time

def test_conflict_scenario():
    primary_mission = Mission(
        id="primary",
        waypoints=[
            Waypoint3D(x=0, y=50, z=10),
            Waypoint3D(x=100, y=50, z=10)
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
    assert conflict_info is not None

def test_no_conflict_scenario():
    mission_A = Mission(
        id="A",
        waypoints=[
            Waypoint3D(x=0, y=0, z=10),
            Waypoint3D(x=100, y=0, z=10)
        ],
        timestamps=[0.0, 10.0]
    )

    mission_B = Mission(
        id="B",
        waypoints=[
            Waypoint3D(x=0, y=10, z=10),
            Waypoint3D(x=100, y=10, z=10)
        ],
        timestamps=[0.0, 10.0]
    )

    conflict_info = find_conflict(mission_A, mission_B, safety_buffer=5.0)
    assert conflict_info is None

def test_near_miss_scenario():
    # Two missions flying parallel, 6 units apart in y, safety buffer is 5.0
    mission_A = Mission(
        id="A",
        waypoints=[
            Waypoint3D(x=0, y=0, z=10),
            Waypoint3D(x=100, y=0, z=10)
        ],
        timestamps=[0.0, 10.0]
    )

    mission_B = Mission(
        id="B",
        waypoints=[
            Waypoint3D(x=0, y=6, z=10),
            Waypoint3D(x=100, y=6, z=10)
        ],
        timestamps=[0.0, 10.0]
    )

    conflict_info = find_conflict(mission_A, mission_B, safety_buffer=5.0)
    assert conflict_info is None

def test_altitude_separation_no_conflict():
    # Two missions cross in X/Y but are separated in Z by more than the safety buffer
    mission_A = Mission(
        id="A",
        waypoints=[
            Waypoint3D(x=0, y=50, z=10),
            Waypoint3D(x=100, y=50, z=10)
        ],
        timestamps=[0.0, 10.0]
    )

    mission_B = Mission(
        id="B",
        waypoints=[
            Waypoint3D(x=50, y=0, z=20),
            Waypoint3D(x=50, y=100, z=20)
        ],
        timestamps=[0.0, 10.0]
    )

    conflict_info = find_conflict(mission_A, mission_B, safety_buffer=5.0)
    assert conflict_info is None

def test_malformed_data_handling():
    # Mission with 3 waypoints but only 2 timestamps (malformed)
    malformed_mission = Mission(
        id="malformed",
        waypoints=[
            Waypoint3D(x=0, y=0, z=10),
            Waypoint3D(x=50, y=50, z=10),
            Waypoint3D(x=100, y=100, z=10)
        ],
        timestamps=[0.0, 10.0]
    )
    # Try to get position at a time that would require interpolation
    with pytest.raises(Exception):
        get_position_at_time(malformed_mission, 5.0)
