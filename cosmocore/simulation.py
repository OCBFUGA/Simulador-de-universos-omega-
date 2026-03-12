import numpy as np
from cosmocore.fields import Fields
from cosmocore.solver import Solver
from cosmocore.physics_laws import DX, DT, NX, compute_qae_epsilon_min

class CosmoCoreSimulation:
    def __init__(self, nx=NX, dx=DX, dt=DT, total_steps=100):
        self.nx = nx
        self.dx = dx
        self.dt = dt
        self.total_steps = total_steps
        self.fields = Fields(self.nx)
        self.solver = Solver(self.fields, self.dt, self.dx)
        self.history = [] # Para armazenar estados em alguns passos

    def run(self):
        print(f"Iniciando simulação CosmoCore com {self.total_steps} passos...")
        print(f"Parâmetros: NX={self.nx}, DX={self.dx}, DT={self.dt}")
        
        # Armazenar o estado inicial
        self._record_state(0)

        for step in range(1, self.total_steps + 1):
            self.solver.step()
            # Armazenar o estado a cada X passos ou no final
            if step % (self.total_steps // 10) == 0 or step == self.total_steps:
                self._record_state(step)
            
            if step % (self.total_steps // 5) == 0:
                print(f"Passo {step}/{self.total_steps} concluído. F[0]={self.fields.F[0]:.6f}")

        print("Simulação CosmoCore concluída!")
        self.print_final_state()

    def _record_state(self, step):
        """Registra o estado atual dos campos para histórico."""
        self.history.append({
            'step': step,
            'F': np.copy(self.fields.F),
            'Psi': np.copy(self.fields.Psi),
            'I': np.copy(self.fields.I),
            'epsilon_min': compute_qae_epsilon_min(self.fields)
        })

    def print_final_state(self):
        print("\n--- Estado Final da Simulação ---")
        final_fields = self.history[-1]
        print(f"Último Passo: {final_fields['step']}")
        print(f"Campo F (primeiros 5): {final_fields['F'][:5]}...")
        print(f"Campo Psi (primeiros 5): {final_fields['Psi'][:5]}...")
        print(f"Campo I (primeiros 5): {final_fields['I'][:5]}...")
        print(f"Epsilon_min (QAE) (primeiros 5): {final_fields['epsilon_min'][:5]}...")

# Função principal para executar a simulação
if __name__ == "__main__":
    sim = CosmoCoreSimulation(total_steps=1000) # Exemplo com 1000 passos
    sim.run()
