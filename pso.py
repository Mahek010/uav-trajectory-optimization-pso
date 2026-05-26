import numpy as np

class ParticleSwarmOptimizer:
    def __init__(self, objective_fn, lower_bounds, upper_bounds, config):
        self.objective_fn = objective_fn
        self.lb = np.asarray(lower_bounds, dtype=float)
        self.ub = np.asarray(upper_bounds, dtype=float)
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def optimize(self):
        cfg = self.config
        dim = len(self.lb)
        positions = self.rng.uniform(self.lb, self.ub, size=(cfg.n_particles, dim))
        velocities = self.rng.normal(0, 0.2, size=(cfg.n_particles, dim))

        personal_best = positions.copy()
        personal_scores = np.array([self.objective_fn(p) for p in positions])
        best_idx = int(np.argmin(personal_scores))
        global_best = personal_best[best_idx].copy()
        global_score = float(personal_scores[best_idx])

        history = []
        for _ in range(cfg.n_iterations):
            r1 = self.rng.random((cfg.n_particles, dim))
            r2 = self.rng.random((cfg.n_particles, dim))
            velocities = (
                cfg.inertia * velocities
                + cfg.cognitive * r1 * (personal_best - positions)
                + cfg.social * r2 * (global_best - positions)
            )
            positions = np.clip(positions + velocities, self.lb, self.ub)

            scores = np.array([self.objective_fn(p) for p in positions])
            improved = scores < personal_scores
            personal_best[improved] = positions[improved]
            personal_scores[improved] = scores[improved]

            best_idx = int(np.argmin(personal_scores))
            if personal_scores[best_idx] < global_score:
                global_score = float(personal_scores[best_idx])
                global_best = personal_best[best_idx].copy()
            history.append(global_score)

        return global_best, global_score, np.array(history)
