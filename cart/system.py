from mechmaths import Expression, Var, Solver
from mechmaths.system import Mass, Spring, Vector, System

Expression.context = ["x", "theta"]
cart = Mass("M")
cart.constrain_plane("x", Vector(1, 0), Vector(0, 0.5))
pendulum = Mass("m")
pendulum.constrain_hinge("theta", Vector(0, -Var("l")), cart.position)
spring = Spring(Vector(-Var("d"), 0.5), cart.position, Var("d"), Var("k"))

system = System(cart, pendulum, spring)
solver = Solver(system.kinetic(), system.potential())
constants = {"M": 1, "m": 1, "g": 10, "l": 1, "d": 1.5, "k": 6}
solver.load_constants(constants)
parameters = [
    {"name": "M", "label": "Cart mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "m", "label": "Pendulum mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
    {"name": "l", "label": "Pendulum length (m)", "min": 0.1, "max": 5, "step": 0.1},
    {"name": "d", "label": "Spring anchor (m)", "min": 0.5, "max": 5, "step": 0.1},
    {"name": "k", "label": "Spring stiffness", "min": 0.1, "max": 100, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [-1, 0.5], None, True, constants, parameters)
