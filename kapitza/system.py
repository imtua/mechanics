from mechmaths import Expression, Var, Solver
from mechmaths.deriv import Sin, Cos


Expression.context = ["theta"]

theta = Var("theta")
t = Var("t")
m = Var("m")
l = Var("l")
a = Var("a")
omega = Var("omega")
vertical_velocity = -a * omega * Sin(omega * t) + l * Sin(theta) * theta.differentiate("t")

kinetic = 0.5 * m * (
    l ** 2 * Cos(theta) ** 2 * theta.differentiate("t") ** 2
    + vertical_velocity ** 2
)
potential = m * Var("g") * (a * Cos(omega * t) - l * Cos(theta))

solver = Solver(kinetic, potential)
constants = {"m": 1, "g": 9.81, "l": 1, "a": 0.15, "omega": 30}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Length (m)", "min": 0.1, "max": 5, "step": 0.1},
    {"name": "a", "label": "Pivot amplitude (m)", "min": 0, "max": 1, "step": 0.01},
    {"name": "omega", "label": "Pivot frequency (rad/s)", "min": 0, "max": 50, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [2.8], None, True, constants, parameters, [0])
