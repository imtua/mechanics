from mechmaths import Expression, Var, Solver
from mechmaths.system import Mass, Vector


Expression.context = ["x1", "x2", "x3"]

m1 = Mass("m1")
m1.constrain_plane("x1", Vector(1, 0), Vector(-2, 0))
m2 = Mass("m2")
m2.constrain_plane("x2", Vector(1, 0), Vector(0, 0))
m3 = Mass("m3")
m3.constrain_plane("x3", Vector(1, 0), Vector(2, 0))

x1 = Var("x1")
x2 = Var("x2")
x3 = Var("x3")
k = Var("k")
potential = 0.5 * k * (x1 ** 2 + (x2 - x1) ** 2 + (x3 - x2) ** 2 + x3 ** 2)
kinetic = m1.kinetic() + m2.kinetic() + m3.kinetic()

solver = Solver(kinetic, potential)
constants = {"m1": 1, "m2": 1, "m3": 1, "k": 8}
solver.load_constants(constants)
parameters = [
    {"name": "m1", "label": "Mass 1 (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "m2", "label": "Mass 2 (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "m3", "label": "Mass 3 (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "k", "label": "Spring stiffness", "min": 0.1, "max": 100, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [0.8, 0, -0.5], None, True, constants, parameters)
