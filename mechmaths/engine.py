from mechmaths.deriv import Variable, Literal, Term, Expression, Sum
from collections import OrderedDict
try:
    import ulab.numpy as np
    import ulab.scipy as sp
    MICROPYTHON = True
except ImportError:
    import numpy as np
    MICROPYTHON = False


def split_variable(term):
    if isinstance(term, Variable) and term.name.endswith("dotdot"):
        return term.name, Literal(1)
    if not isinstance(term, Term):
        return None, term
    for subterm in term.terms:
        if isinstance(subterm, Variable) and subterm.name.endswith("dotdot"):
            newterms = term.terms.copy()
            newterms.remove(subterm)
            if not newterms:
                return subterm.name, Literal(term.coeff)
            return subterm.name, Term(term.coeff, newterms)
    return None, term


def euler_lagrange(lagrangian):
    eqs = []
    for variable in Expression.context:
        term1 = lagrangian.differentiate(variable + "dot").differentiate("t")
        term2 = lagrangian.differentiate(variable)
        eq = (term1 - term2).substitute({})

        coeffs = OrderedDict()
        for variable in Expression.context:
            coeffs[variable + "dotdot"] = []
        coeffs[None] = []
        for term in eq.terms:
            name, term = split_variable(term)
            coeffs[name].append(term)

        row = []
        for name in coeffs:
            if coeffs[name]:
                row.append(Sum(coeffs[name]).substitute({}))
            else:
                row.append(Literal(0))
        eqs.append(row)
    return eqs


if MICROPYTHON:
    def solve_system(a, b):
        if a.shape == (1, 1):
            return [b[0] / a[0, 0]]
        if a.shape == (2, 2):
            det = a[0, 0] * a[1, 1] - a[0, 1] * a[1, 0]
            x1 = (a[1, 1] * b[0] - a[1, 0] * b[1]) / det
            x2 = (-a[0, 1] * b[0] + a[0, 0] * b[1]) / det
            return [x1, x2]

        try:
            L = np.linalg.cholesky(a)
            return sp.linalg.cho_solve(L, b)
        except ValueError:
            L = np.linalg.cholesky(-a)
            return sp.linalg.cho_solve(L, -b)
else:
    def solve_system(a, b):
        return np.linalg.solve(a, b)


class Solver:
    def __init__(self, kinetic, potential):
        self.original = (kinetic, potential)
        self.kinetic = None
        self.potential = None
        self.lagrangian = None
        self.motion_eqs = None
        self.context = Expression.context
        self.degrees = len(self.context)
        self.phase = np.zeros((2, self.degrees))
        self.time = 0

    def load_constants(self, values):
        self.kinetic = self.original[0].substitute(values)
        self.potential = self.original[1].substitute(values)
        self.lagrangian = self.kinetic - self.potential
        self.motion_eqs = euler_lagrange(self.lagrangian)

    def load_initial_values(self, params, param_derivs=None):
        self.phase = np.zeros((2, self.degrees))
        self.phase[0] = params
        if param_derivs is not None:
            self.phase[1] = param_derivs
        self.time = 0

    def get_solver_values(self, phase, t):
        values = {"t": t}
        for i, name in enumerate(self.context):
            values[name] = phase[0][i]
            values[name + "dot"] = phase[1][i]
        return values

    def gradient(self, phase, t):
        values = self.get_solver_values(phase, t)
        matrix = np.zeros((self.degrees, self.degrees))
        constants = np.zeros((self.degrees,))
        for i in range(self.degrees):
            for j in range(i, self.degrees):
                matrix[i, j] = self.motion_eqs[i][j].evaluate(values)
                matrix[j, i] = matrix[i, j]
            constants[i] = -self.motion_eqs[i][self.degrees].evaluate(values)
        accelerations = solve_system(matrix, constants)
        return np.array([phase[1], accelerations])

    def step(self, dt):
        k1 = dt * self.gradient(self.phase, self.time)
        k2 = dt * self.gradient(self.phase + k1 / 2, self.time + dt / 2)
        k3 = dt * self.gradient(self.phase + k2 / 2, self.time + dt / 2)
        k4 = dt * self.gradient(self.phase + k3, self.time + dt)
        self.phase += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.time += dt

    def get_params(self):
        return self.phase[0].tolist()

    def get_energies(self):
        values = self.get_solver_values(self.phase, self.time)
        kinetic = self.kinetic.evaluate(values)
        potential = self.potential.evaluate(values)
        return (kinetic, potential)

    def display_equations(self):
        lines = []
        for row in self.motion_eqs:
            line = ""
            for i in range(len(Expression.context)):
                variable = str(Variable(Expression.context[i] + "dotdot"))
                line += str(row[i]) + variable
                if Expression.latex_mode:
                    line += "&\\\\"
                line += " + "
            line += str(row[-1])
            if Expression.latex_mode:
                line += "&"
            line += " = 0"
            lines.append(line.replace("+ -", "- "))
        return lines
