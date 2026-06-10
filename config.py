from dataclasses import dataclass
import numpy as np

@dataclass
class ObjectiveWeights:
    distance: float = 1.0
    energy: float = 1.8
    smoothness: float = 7.0
    collision: float = 900.0
    boundary: float = 500.0

@dataclass
class PSOConfig:
    n_particles: int = 80
    n_iterations: int = 220
    inertia: float = 0.72
    cognitive: float = 1.45
    social: float = 1.45
    seed: int = 42

@dataclass
class ScenarioConfig:
    start: np.ndarray
    goal: np.ndarray
    bounds: tuple
    n_waypoints: int = 7
    safety_margin: float = 0.45


def default_scenario() -> ScenarioConfig:
    return ScenarioConfig(
        start=np.array([0.5, 0.5]),
        goal=np.array([9.5, 8.5]),
        bounds=((0.0, 10.0), (0.0, 10.0)),
        n_waypoints=7,
        safety_margin=0.45,
    )
