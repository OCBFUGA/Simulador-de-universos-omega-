import numpy as np

class Fields:
    def __init__(self, nx):
        self.nx = nx
        self.F = np.random.rand(nx) # Campo de auto-organização
        self.Psi = np.random.rand(nx) + 1j * np.random.rand(nx) # Campo de percepção/matéria (complexo)
        self.I = np.random.rand(nx) # Densidade informacional
