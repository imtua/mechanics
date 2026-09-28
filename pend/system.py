from mechmaths import Expression, Var, Solver
from mechmaths.system import Mass, Vector, System

Expression.context = ["theta"]
mass = Mass("m")
mass.constrain_hinge("theta", Vector(0, -Var("l")), Vector(0, Var("l")))

system = System(mass)
solver = Solver(system.kinetic(), system.potential())
constants = {"m": 1, "g": 10, "l": 1}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Length (m)", "min": 0.1, "max": 5, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [2], None, True, constants, parameters)
