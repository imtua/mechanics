from mechmaths import Expression, Var, Solver
from mechmaths.deriv import Sin, Cos


Expression.context = ["theta", "phi"]

theta = Var("theta")
phi = Var("phi")
m = Var("m")
l = Var("l")
kinetic = 0.5 * m * l ** 2 * (
    theta.differentiate("t") ** 2 + Sin(theta) ** 2 * phi.differentiate("t") ** 2
)
potential = -m * Var("g") * l * Cos(theta)

solver = Solver(kinetic, potential)
constants = {"m": 1, "g": 9.81, "l": 1}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Length (m)", "min": 0.1, "max": 5, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(
        solver, [0.9, 0], None, True, constants, parameters, [0, 2.5]
    )
