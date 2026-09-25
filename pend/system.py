from mechsim import Expression, Var, Solver
from mechsim.system import Mass, Vector, System

Expression.context = ["theta"]
mass = Mass("m")
mass.constrain_hinge("theta", Vector(0, -Var("l")), Vector(0, Var("l")))

system = System(mass)
solver = Solver(system.kinetic(), system.potential())
solver.load_constants({"m": 1, "g": 10, "l": 1})

if __name__ == "__main__":
    from runner import load_solver
    load_solver(solver, [2])
