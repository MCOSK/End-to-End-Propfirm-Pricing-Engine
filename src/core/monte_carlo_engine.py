import numpy as np

class MonteCarloEngine:
    """
    Moteur de simulation stochastique vectorisé par Euler-Maruyama 
    pour le pricing d'options à barrière path-dependent.
    """
    def __init__(self, n_paths: int = 10000, n_steps: int = 1000, dt: float = 1.0):
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.dt = dt

    def simulate_paths(self, initial_capital: float, mu: float, sigma: float) -> np.ndarray:
        """
        Génère la matrice N x T des trajectoires de capital (Mouvement Brownien Arithmétique).
        """
        # Génération de la matrice des chocs gaussiens Z ~ N(0,1)
        Z = np.random.normal(0, 1, (self.n_paths, self.n_steps))
        
        # Application du schéma d'Euler-Maruyama vectorisé
        increments = mu * self.dt + sigma * np.sqrt(self.dt) * Z
        
        # Construction des trajectoires via somme cumulative
        # On insère le capital initial à t=0
        paths = np.zeros((self.n_paths, self.n_steps + 1))
        paths[:, 0] = initial_capital
        paths[:, 1:] = initial_capital + np.cumsum(increments, axis=1)
        
        return paths

    def calculate_trailing_drawdown_ruin(self, paths: np.ndarray, drawdown_limit: float) -> dict:
        """
        Évalue la matrice des trajectoires face à une barrière mobile (Trailing Drawdown).
        Retourne la probabilité de ruine empirique et les temps d'arrêt tau.
        """
        # Matrice M_t : High-Water Mark cumulatif pour chaque instant t
        running_max = np.maximum.accumulate(paths, axis=1)
        
        # Matrice D_t : La barrière suiveuse
        trailing_barrier = running_max - drawdown_limit
        
        # Matrice booléenne des franchissements de barrière
        ruin_mask = paths <= trailing_barrier
        
        # Identification du premier instant de ruine pour chaque trajectoire
        # np.argmax retourne le premier True. Si aucun True, retourne 0.
        tau = np.argmax(ruin_mask, axis=1)
        
        # Correction pour les trajectoires qui ne ruinent jamais
        # Si tau == 0 et que l'instant 0 n'est pas une ruine, la trajectoire a survécu
        survived_mask = (tau == 0) & (~ruin_mask[:, 0])
        tau[survived_mask] = paths.shape[1]  # Le temps d'arrêt est repoussé à l'infini (ou fin de simulation)
        
        ruin_probability = 1.0 - (np.sum(survived_mask) / self.n_paths)
        
        return {
            "ruin_probability": round(ruin_probability, 4),
            "survival_probability": round(1.0 - ruin_probability, 4),
            "stopping_times": tau
        }

# --- TEST NUMÉRIQUE ---
if __name__ == "__main__":
    # Paramètres d'une évaluation standard (ex: 50k, Trailing DD de 2500)
    engine = MonteCarloEngine(n_paths=10000, n_steps=2000, dt=1.0)
    
    # Trader avec Edge nul (Jeu à somme nulle, bruit pur)
    print("Simulation de 10 000 trajectoires en cours...")
    paths = engine.simulate_paths(initial_capital=50000, mu=0.0, sigma=50.0) # sigma = 50€ par pas
    
    results = engine.calculate_trailing_drawdown_ruin(paths, drawdown_limit=2500)
    
    print(f"Probabilité empirique de ruine (Trailing DD) : {results['ruin_probability'] * 100}%")
