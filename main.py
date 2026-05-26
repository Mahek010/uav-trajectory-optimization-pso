from pathlib import Path
import numpy as np
import pandas as pd

from .config import ObjectiveWeights, PSOConfig, default_scenario
from .environment import default_obstacles, make_path_from_vector
from .objective import objective, path_length, energy_proxy, collision_penalty
from .pso import ParticleSwarmOptimizer
from .visualization import plot_trajectory, plot_convergence


def run(output_dir="results"):
    output_dir = Path(output_dir)
    scenario = default_scenario()
    obstacles = default_obstacles()
    weights = ObjectiveWeights()
    pso_cfg = PSOConfig()

    (xmin, xmax), (ymin, ymax) = scenario.bounds
    lower = np.array([xmin, ymin] * scenario.n_waypoints)
    upper = np.array([xmax, ymax] * scenario.n_waypoints)

    fn = lambda v: objective(v, scenario, obstacles, weights)
    optimizer = ParticleSwarmOptimizer(fn, lower, upper, pso_cfg)
    best_vector, best_score, history = optimizer.optimize()

    optimized_path = make_path_from_vector(best_vector, scenario.start, scenario.goal)
    baseline = np.linspace(scenario.start, scenario.goal, scenario.n_waypoints + 2)

    output_dir.mkdir(parents=True, exist_ok=True)
    plot_trajectory(optimized_path, baseline, obstacles, scenario, output_dir / "trajectory_comparison.png")
    plot_convergence(history, output_dir / "convergence.png")

    pd.DataFrame(optimized_path, columns=["x", "y"]).to_csv(output_dir / "optimized_path.csv", index=False)

    summary = {
        "best_objective": best_score,
        "optimized_distance": path_length(optimized_path),
        "baseline_distance": path_length(baseline),
        "optimized_energy_proxy": energy_proxy(optimized_path),
        "baseline_energy_proxy": energy_proxy(baseline),
        "optimized_collision_penalty": collision_penalty(optimized_path, obstacles, scenario.safety_margin),
        "baseline_collision_penalty": collision_penalty(baseline, obstacles, scenario.safety_margin),
    }
    pd.DataFrame([summary]).to_csv(output_dir / "summary_metrics.csv", index=False)
    return summary


if __name__ == "__main__":
    metrics = run()
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
