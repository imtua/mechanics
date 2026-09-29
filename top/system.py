from mechmaths import Expression, Var, Solver
from mechmaths.deriv import Sin, Cos


Expression.context = ["theta", "phi", "psi"]

theta = Var("theta")
phi = Var("phi")
psi = Var("psi")
m = Var("m")
g = Var("g")
l = Var("l")
I1 = Var("I1")
I3 = Var("I3")

theta_dot = theta.differentiate("t")
phi_dot = phi.differentiate("t")
psi_dot = psi.differentiate("t")
spin_rate = psi_dot + Cos(theta) * phi_dot
kinetic = 0.5 * I1 * (theta_dot ** 2 + Sin(theta) ** 2 * phi_dot ** 2)
kinetic += 0.5 * I3 * spin_rate ** 2
potential = m * g * l * Cos(theta)

solver = Solver(kinetic, potential)
constants = {"m": 1, "g": 9.81, "l": 0.5, "I1": 0.08, "I3": 0.04}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Center-of-mass length (m)", "min": 0.1, "max": 2, "step": 0.1},
    {"name": "I1", "label": "Transverse inertia", "min": 0.001, "max": 10, "step": 0.001},
    {"name": "I3", "label": "Axial inertia", "min": 0.001, "max": 10, "step": 0.001},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(
        solver, [0.75, 0, 0], None, True, constants, parameters,
        [0.0, 8.0, 35.0]
    )
