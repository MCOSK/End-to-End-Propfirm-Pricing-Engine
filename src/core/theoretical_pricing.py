import numpy as np

class CompoundOptionPricer:
    """
    Modélisation analytique d'une évaluation Prop Firm en 2 étapes
    basée sur les probabilités d'atteinte d'un Mouvement Brownien.
    """
    def __init__(self, initial_capital: float = 100000.0):
        self.X0 = initial_capital

    def hitting_probability(self, target_pct: float, max_loss_pct: float, mu: float, sigma: float) -> float:
        """
        Calcule P(tau_K < tau_D) analytiquement.
        mu: Dérive par trade (Edge net après frais).
        sigma: Bruit/Risque par trade.
        """
        a = target_pct  # Distance à l'objectif
        b = max_loss_pct # Distance à la ruine
        
        # Cas limite : Marche aléatoire pure (Edge nul)
        if np.isclose(mu, 0.0, atol=1e-8):
            return b / (a + b)
            
        # Facteur de l'équation d'Itô : 2 * mu / sigma^2
        ratio = (2 * mu) / (sigma ** 2)
        
        numerator = 1 - np.exp(-ratio * b)
        denominator = 1 - np.exp(-ratio * (a + b))
        
        # Sécurité mathématique contre les divisions par zéro
        if np.isclose(denominator, 0.0):
            return 0.0
            
        return numerator / denominator

    def evaluate_two_step_prop_firm(self, target_1: float, target_2: float, max_loss: float, mu: float, sigma: float) -> dict:
        """
        Calcule la probabilité de réussite globale de l'option composée.
        """
        p_phase1 = self.hitting_probability(target_1, max_loss, mu, sigma)
        p_phase2 = self.hitting_probability(target_2, max_loss, mu, sigma)
        
        p_global = p_phase1 * p_phase2
        
        return {
            "P(Phase 1)": round(p_phase1, 4),
            "P(Phase 2)": round(p_phase2, 4),
            "P(Global_Funding)": round(p_global, 4)
        }

# --- TEST ANALYTIQUE ---
if __name__ == "__main__":
    pricer = CompoundOptionPricer()
    
    # Paramètres FTMO Classiques
    t1, t2, loss = 0.10, 0.05, 0.10
    
    # Scénario A : Trader avec Edge nul (Jeu à somme nulle)
    res_zero = pricer.evaluate_two_step_prop_firm(t1, t2, loss, mu=0.0, sigma=0.01)
    print("Edge Nul (mu=0) :", res_zero)
    
    # Scénario B : Trader impacté par le spread/frais (Dérive négative)
    res_negative = pricer.evaluate_two_step_prop_firm(t1, t2, loss, mu=-0.001, sigma=0.01)
    print("Friction de Marché (mu=-0.001) :", res_negative)
    
    # Scénario C : Quant avec un léger Edge (Dérive positive)
    res_positive = pricer.evaluate_two_step_prop_firm(t1, t2, loss, mu=0.001, sigma=0.01)
    print("Quant Edge (mu=0.001) :", res_positive)




def evaluate_two_step_prop_firm(self, target_1: float, target_2: float, max_loss_global: float, max_loss_daily: float, mu: float, sigma: float) -> dict:
        """
        Calcule la probabilité de réussite globale en intégrant la dominance de la barrière journalière.
        """
        # La barrière effective qui tue le trader au démarrage est la barrière journalière.
        effective_loss_barrier = min(max_loss_global, max_loss_daily)
        
        # Phase 1 : Objectif vs Barrière effective
        p_phase1 = self.hitting_probability(target_1, effective_loss_barrier, mu, sigma)
        
        # Phase 2 : Objectif réduit vs Barrière effective
        p_phase2 = self.hitting_probability(target_2, effective_loss_barrier, mu, sigma)
        
        # Option Composée : Produit des probabilités
        p_global = p_phase1 * p_phase2
        
        return {
            "Barriere_Effective": effective_loss_barrier,
            "P(Phase 1)": round(p_phase1, 4),
            "P(Phase 2)": round(p_phase2, 4),
            "P(Global_Funding)": round(p_global, 4)
        }
