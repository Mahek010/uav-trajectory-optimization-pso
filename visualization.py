from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def plot_trajectory(path, baseline, obstacles, scenario, save_path):
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(baseline[:, 0], baseline[:, 1], '--', label='Baseline straight path')
    ax.plot(path[:, 0], path[:, 1], '-o', label='Optimized PSO path')
    ax.scatter([scenario.start[0]], [scenario.start[1]], s=90, marker='s', label='Start')
    ax.scatter([scenario.goal[0]], [scenario.goal[1]], s=90, marker='*', label='Goal')

    for obs in obstacles:
        ax.add_patch(Circle(obs.center, obs.radius, fill=False, linewidth=2))
        ax.add_patch(Circle(obs.center, obs.radius + scenario.safety_margin, fill=False, linestyle=':', linewidth=1))
        ax.text(obs.center[0], obs.center[1], obs.name, ha='center', va='center', fontsize=8)

    (xmin, xmax), (ymin, ymax) = scenario.bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('X position [km]')
    ax.set_ylabel('Y position [km]')
    ax.set_title('UAV trajectory optimization using PSO')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(save_path, dpi=200)
    plt.close(fig)


def plot_convergence(history, save_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.arange(1, len(history) + 1), history)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Best objective value')
    ax.set_title('PSO convergence')
    ax.grid(True, alpha=0.3)
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(save_path, dpi=200)
    plt.close(fig)
