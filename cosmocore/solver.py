import numpy as np
from cosmocore.physics_laws import Fields, evolve_laca, evolve_dpm, evolve_tdl

class Solver:
    def __init__(self, fields: Fields, dt: float, dx: float):
        self.fields = fields
        self.dt = dt
        self.dx = dx

    def step(self):
        """Avança a simulação em um passo de tempo usando o método de Euler."""
        # Evolui os campos usando as leis computáveis
        # A ordem de evolução pode ser importante em sistemas acoplados.
        # Para esta versão simplificada, evoluímos sequencialmente.
        self.fields.F = evolve_laca(self.fields, self.dt, self.dx)
        self.fields.Psi = evolve_dpm(self.fields, self.dt)
        self.fields.I = evolve_tdl(self.fields, self.dt)

        # GIM e QAE são mais sobre cálculos de valores/correções do que evolução direta de campo neste nível.
        # Se GIM fosse uma equação de campo para g_mu_nu, precisaria de um solver dedicado.
        # QAE calcula epsilon_min com base nos campos atuais.

# --- Main para teste rápido (remova na integração) ---
if __name__ == "__main__":
    print("Testando solver.py...")
    from cosmocore.physics_laws import NX, DT, DX
    
    fields = Fields(NX)
    solver = Solver(fields, DT, DX)
    
    print(f"Campos F iniciais: {fields.F[:5]}...")
    
    # Executar 10 passos da simulação
    for i in range(10):
        solver.step()
        # print(f"Passo {i+1}: F[0]={fields.F[0]:.6f}, Psi[0]={fields.Psi[0]:.6f}, I[0]={fields.I[0]:.6f}")
        
    print(f"Campos F após 10 passos: {fields.F[:5]}...")
    
    # Exemplo de cálculo QAE após a simulação
    from cosmocore.physics_laws import compute_qae_epsilon_min
    epsilon_min_values = compute_qae_epsilon_min(fields)
    print(f"Epsilon_min (QAE) para os primeiros 5 pontos: {epsilon_min_values[:5]}...")
