from mechmaths import Expression, Var, Solver
from mechmaths.system import Vector, Mass, System
import math

Expression.context = ["r", "theta"]
mass1 = Mass("M")
mass1.constrain_plane("r", Vector(0, 1))
mass2 = Mass("m")
mass2.constrain_hinge("theta", Vector(0, -Var("r")), Vector(2, 0))

system = System(mass1, mass2)
solver = Solver(system.kinetic(), system.potential())
solver.load_constants({
    "m": 1, "M": 5, "g": 10
})

if __name__ == "__main__":
    from runner import load_solver
    load_solver(solver, [1, math.pi / 2])
