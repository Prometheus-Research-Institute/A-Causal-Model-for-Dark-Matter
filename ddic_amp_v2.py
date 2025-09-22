import numpy as np
from datetime import datetime

# ==============================================================================
# COMPUTATIONAL ARTIFACT: ANNUAL MODULATION PREDICTOR (AMP-2026)
# Version: 2.0 (Revised)
# Authors: Prometheus Research
# ==============================================================================

class AnnualModulationPredictor:
    """
    Implements the predictive model for dark matter annual modulation
    based on the density-dependent phase transition model.
    """

    def __init__(self, year=2026):
        """
        Initializes the model parameters for a specific year.
        """
        self.target_year = year
        # Parameters of the main overdensity filament
        self.filament_peak_day_of_year = 155  # Day of the year for the density peak (June 4th)
        self.filament_width_days = 15          # Characteristic width of the filament in days
        self.density_enhancement_factor = 8.5  # Density enhancement factor at the peak
        
        # Parameters of the phase transition model
        self.rho_crit_normalized = 5.0         # Critical transition density (in normalized model units)
        self.k_factor = 2.5                    # Steepness factor of the transition

    def get_relative_density_at_date(self, date_obj):
        """
        Calculates the relative dark matter density at Earth's position
        for a given date.
        """
        day_of_year = date_obj.timetuple().tm_yday
        exponent = -0.5 * ((day_of_year - self.filament_peak_day_of_year) / self.filament_width_days)**2
        density = 1 + (self.density_enhancement_factor - 1) * np.exp(exponent)
        return density

    def get_phase_transition_probability(self, density):
        """
        Calculates the phase transition probability based on the local density.
        """
        if density < self.rho_crit_normalized:
            return 0.0
        arg = self.k_factor * (density / self.rho_crit_normalized - 1)
        probability = np.tanh(arg)
        return probability

    def predict_relative_signal_rate(self, date_str):
        """
        Predicts the expected relative event rate for a specific date.
        """
        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d')
            if input_date.year != self.target_year:
                return {"warning": f"This predictor is calibrated for {self.target_year}."}
        except ValueError:
            return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}

        local_density = self.get_relative_density_at_date(input_date)
        transition_prob = self.get_phase_transition_probability(local_density)
        signal_rate = 1.0 + 100 * transition_prob
        return signal_rate

# --- Usage Example ---
# predictor_2026 = AnnualModulationPredictor(year=2026)
# date_peak = "2026-06-04"
# rate_peak = predictor_2026.predict_relative_signal_rate(date_peak)
# print(f"Predicted relative event rate for {date_peak}: {rate_peak:.2f}")
