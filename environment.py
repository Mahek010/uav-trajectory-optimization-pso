from dataclasses import dataclass
import numpy as np

@dataclass
class CircularObstacle:
    center: np.ndarray
    radius: float
    name: str = "obstacle"


def default_obstacles():
    return [
        CircularObstacle(np.array([3.0, 3.2]), 1.05, "Building A"),
        CircularObstacle(np.array([5.3, 5.4]), 1.15, "No-fly zone"),
        CircularObstacle(np.array([7.2, 3.0]), 0.95, "Tower"),
        CircularObstacle(np.array([6.4, 7.4]), 0.85, "Restricted area"),
    ]


def interpolate_path(path: np.ndarray, samples_per_segment: int = 25) -> np.ndarray:
    samples = []
    for p0, p1 in zip(path[:-1], path[1:]):
        t = np.linspace(0, 1, samples_per_segment, endpoint=False)
        samples.append(p0[None, :] * (1 - t[:, None]) + p1[None, :] * t[:, None])
    samples.append(path[-1][None, :])
    return np.vstack(samples)


def make_path_from_vector(vector: np.ndarray, start: np.ndarray, goal: np.ndarray) -> np.ndarray:
    waypoints = vector.reshape(-1, 2)
    return np.vstack([start, waypoints, goal])
