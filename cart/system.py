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
solver.load_constants({"M": 1, "m": 1, "g": 10, "l": 1, "d": 1.5, "k": 6})

if __name__ == "__main__":
    from runner import load_solver
    load_solver(solver, [-1, 0.5])
