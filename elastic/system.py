from mechmaths import Expression, Var, Solver
from mechmaths.system import Mass, Spring, Vector, System

Expression.context = ["r", "theta"]

mass = Mass("m")
mass.constrain_hinge("theta", Vector(0, -Var("r")), Vector(0, 0))
spring = Spring(Vector(0, 0), mass.position, Var("l"), Var("k"))

system = System(mass, spring)
solver = Solver(system.kinetic(), system.potential())
constants = {"m": 1, "g": 10, "l": 1, "k": 20}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Rest length (m)", "min": 0.1, "max": 3, "step": 0.1},
    {"name": "k", "label": "Spring stiffness", "min": 0.1, "max": 100, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [1, 0.8], None, True, constants, parameters)
