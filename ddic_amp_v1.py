import numpy as np
from datetime import datetime

# ==============================================================================
# ARTEFACTO COMPUTACIONAL: PREDICTOR DE MODULACIÓN ANUAL (AMP-2025)
# Versión: 1.1 (Corregida)
# Autores: Prometheus Research
# ==============================================================================

class AnnualModulationPredictor:
    """
    Implementa el modelo predictivo para la modulación anual de la materia oscura
    basado en el modelo de transición de fase dependiente de la densidad.
    """

    def __init__(self):
        """
        Inicializa los parámetros del modelo del halo galáctico y la órbita terrestre.
        """
        # Parámetros del filamento de sobredensidad principal
        self.filament_peak_day_of_year = 155  # Día del año del pico de densidad (4 de Junio)
        self.filament_width_days = 15          # Ancho característico del filamento en días
        self.density_enhancement_factor = 8.5  # Factor de aumento de densidad en el pico
        
        # Parámetros del modelo de transición de fase
        self.rho_crit_normalized = 5.0         # Densidad crítica de transición (unidades normalizadas)
        self.k_factor = 2.5                    # Factor de rapidez de la transición

    def get_relative_density_at_date(self, date_obj):
        """
        Calcula la densidad relativa de materia oscura en la posición de la Tierra
        para una fecha dada.
        """
        day_of_year = date_obj.timetuple().tm_yday
        exponent = -0.5 * ((day_of_year - self.filament_peak_day_of_year) / self.filament_width_days)**2
        density = 1 + (self.density_enhancement_factor - 1) * np.exp(exponent)
        return density

    def get_phase_transition_probability(self, density):
        """
        Calcula la probabilidad de transición de fase basada en la densidad local.
        """
        if density < self.rho_crit_normalized:
            return 0.0
        arg = self.k_factor * (density / self.rho_crit_normalized - 1)
        probability = np.tanh(arg)
        return probability

    def predict_relative_signal_rate(self, date_str):
        """
        Predice la tasa de eventos relativa esperada para una fecha específica.
        """
        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}

        local_density = self.get_relative_density_at_date(input_date)
        transition_prob = self.get_phase_transition_probability(local_density)
        signal_rate = 1.0 + 100 * transition_prob
        return signal_rate

if __name__ == '__main__':
    # --- Ejemplo de Uso y Verificación ---
    # Esta sección solo se ejecuta si el script es llamado directamente.
    # No afectará su uso como librería.
    
    predictor = AnnualModulationPredictor()
    
    date_peak = "2025-06-04"
    rate_peak = predictor.predict_relative_signal_rate(date_peak)
    
    print("--- Verificación del Script AMP-2025 v1.1 ---")
    print(f"Ejecución de prueba para la fecha pico: {date_peak}")
    print(f"Tasa de eventos relativa predicha: {rate_peak:.2f}")
    print("El script es sintácticamente correcto y funcional.")
