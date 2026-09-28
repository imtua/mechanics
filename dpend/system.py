from mechmaths import Expression, Var, Solver
from mechmaths.system import Mass, Vector, System

Expression.context = ["theta1", "theta2"]
height = Var("l1") + Var("l2")
mass1 = Mass("m1")
mass1.constrain_hinge("theta1", Vector(0, -Var("l1")), Vector(0, height))
mass2 = Mass("m2")
mass2.constrain_hinge("theta2", Vector(0, -Var("l2")), mass1.position)

system = System(mass1, mass2)
solver = Solver(system.kinetic(), system.potential())
constants = {"m1": 1, "m2": 1.0, "g": 10, "l1": 0.5, "l2": 0.5}
solver.load_constants(constants)
parameters = [
    {"name": "m1", "label": "Mass 1 (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "m2", "label": "Mass 2 (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l1", "label": "Length 1 (m)", "min": 0.1, "max": 3, "step": 0.1},
    {"name": "l2", "label": "Length 2 (m)", "min": 0.1, "max": 3, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [2, 3.14], None, True, constants, parameters)
