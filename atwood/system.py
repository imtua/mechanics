from mechmaths import Expression, Var, Solver
from mechmaths.system import Vector, Mass, System
import math

Expression.context = ["r", "theta"]
mass1 = Mass("M")
mass1.constrain_plane("r", Vector(0, 1))
mass2 = Mass("m")
mass2.constrain_hinge("theta", Vector(0, -Var("r")), Vector(2, 0))

system = System(mass1, mass2)
solver = Solver(system.kinetic(), system.potential())
constants = {"m": 1, "M": 5, "g": 10}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Swinging mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "M", "label": "Hanging mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [1, math.pi / 2], None, True, constants, parameters)
