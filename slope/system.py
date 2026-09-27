from mechmaths import Expression, Var, Solver
from mechmaths.system import Vector, Disk, System

Expression.context = ["x"]
disk = Disk("m", "I", Var("r"))
disk.constrain_plane("x", Vector(2, -1))

system = System(disk)
solver = Solver(system.kinetic(), system.potential())
solver.load_constants({
    "m": 1, "I": 1, "g": 10
})

if __name__ == "__main__":
    from runner import load_solver
    load_solver(solver, [-7])
