import numpy as np
from .environment import interpolate_path, make_path_from_vector


def path_length(path: np.ndarray) -> float:
    return float(np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1)))


def smoothness_penalty(path: np.ndarray) -> float:
    vectors = np.diff(path, axis=0)
    penalty = 0.0
    for i in range(len(vectors) - 1):
        a, b = vectors[i], vectors[i + 1]
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na < 1e-9 or nb < 1e-9:
            continue
        cos_angle = np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0)
        angle = np.arccos(cos_angle)
        penalty += angle ** 2
    return float(penalty)


def energy_proxy(path: np.ndarray) -> float:
    segment_lengths = np.linalg.norm(np.diff(path, axis=0), axis=1)
    speed_change_proxy = np.sum(np.abs(np.diff(segment_lengths)))
    turning_energy = smoothness_penalty(path)
    return float(np.sum(segment_lengths ** 1.12) + 0.65 * speed_change_proxy + 0.35 * turning_energy)


def collision_penalty(path: np.ndarray, obstacles, safety_margin: float) -> float:
    sampled = interpolate_path(path, samples_per_segment=35)
    penalty = 0.0
    for obs in obstacles:
        d = np.linalg.norm(sampled - obs.center, axis=1)
        clearance = d - (obs.radius + safety_margin)
        violation = np.maximum(0.0, -clearance)
        penalty += np.sum(violation ** 2)
    return float(penalty)


def boundary_penalty(path: np.ndarray, bounds) -> float:
    (xmin, xmax), (ymin, ymax) = bounds
    x, y = path[:, 0], path[:, 1]
    px = np.maximum(0, xmin - x) + np.maximum(0, x - xmax)
    py = np.maximum(0, ymin - y) + np.maximum(0, y - ymax)
    return float(np.sum(px ** 2 + py ** 2))


def progress_penalty(path: np.ndarray) -> float:
    """Penalize backward movement along the start-to-goal direction to avoid unrealistic loops."""
    direction = path[-1] - path[0]
    norm = np.linalg.norm(direction)
    if norm < 1e-9:
        return 0.0
    unit = direction / norm
    projected_steps = np.diff(path, axis=0) @ unit
    backward = np.maximum(0.0, -projected_steps)
    return float(np.sum(backward ** 2))


def objective(vector, scenario, obstacles, weights):
    path = make_path_from_vector(vector, scenario.start, scenario.goal)
    return (
        weights.distance * path_length(path)
        + weights.energy * energy_proxy(path)
        + weights.smoothness * smoothness_penalty(path)
        + weights.collision * collision_penalty(path, obstacles, scenario.safety_margin)
        + weights.boundary * boundary_penalty(path, scenario.bounds)
        + 600.0 * progress_penalty(path)
    )
