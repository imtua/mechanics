from mechmaths import Expression, Var, Solver
from mechmaths.deriv import Sin, Cos


Expression.context = ["theta"]

theta = Var("theta")
mass = Var("m")
radius = Var("R")
angular_speed = Var("omega")

kinetic = 0.5 * mass * radius ** 2 * (
    theta.differentiate("t") ** 2 + angular_speed ** 2 * Sin(theta) ** 2
)
potential = -mass * Var("g") * radius * Cos(theta)

solver = Solver(kinetic, potential)
constants = {"m": 1, "g": 9.81, "R": 1, "omega": 3}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Bead mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "R", "label": "Hoop radius (m)", "min": 0.1, "max": 5, "step": 0.1},
    {"name": "omega", "label": "Hoop speed (rad/s)", "min": 0, "max": 10, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [0.8], None, True, constants, parameters)
