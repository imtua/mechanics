from mechmaths import Expression, Var, Solver
from mechmaths.system import Vector, Disk, System

Expression.context = ["x"]
disk = Disk("m", "I", Var("r"))
disk.constrain_plane("x", Vector(2, -1))

system = System(disk)
solver = Solver(system.kinetic(), system.potential())
constants = {"m": 1, "I": 1, "r": 1, "g": 10}
solver.load_constants(constants)
parameters = [
    {"name": "m", "label": "Disk mass (kg)", "min": 0.1, "max": 20, "step": 0.1},
    {"name": "I", "label": "Moment of inertia", "min": 0.001, "max": 10, "step": 0.001},
    {"name": "r", "label": "Radius (m)", "min": 0.05, "max": 2, "step": 0.05},
    {"name": "g", "label": "Gravity (m/s²)", "min": 0.1, "max": 30, "step": 0.1},
]

if __name__ == "__main__":
    from simulation_runner import load_solver
    load_solver(solver, [-7], None, True, constants, parameters)
