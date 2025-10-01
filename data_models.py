from dataclasses import dataclass
from typing import List

@dataclass
class Waypoint3D:
    x: float
    y: float
    z: float

@dataclass
class Mission:
    id: str
    waypoints: List[Waypoint3D]
    timestamps: List[float]
