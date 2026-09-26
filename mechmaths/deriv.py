import math
from collections import OrderedDict

denominator_limit = 100


def get_fraction(value):
    differences = [1]
    for i in range(1, denominator_limit + 1):
        top = value * i
        differences.append(abs(top - round(top)))
    bottom = differences.index(min(differences))
    return round(value * bottom), bottom


def format_number(value):
    if not Expression.latex_mode:
        return str(value)

    n, d = get_fraction(value)
    if d == 1:
        return str(n)
    if n < 0:
        return "-\\frac{" + str(-n) + "}{" + str(d) + "}"
    else:
        return "\\frac{" + str(n) + "}{" + str(d) + "}"


def format_variable(name):
    if not Expression.latex_mode:
        return name

    subscript = ""
    if "_" in name:
        subscript = name[name.index("_"):]
        name = name[:name.index("_")]
    else:
        counter = 0
        while counter < len(name):
            if name[counter].isdigit():
                break
            counter += 1
        if counter < len(name):
            subscript = "_" + name[counter:]
            name = name[:counter]
    if len(name) > 1:
        name = "\\" + name
    return name + subscript


def cartesian_product(*iterables):
    pools = [tuple(pool) for pool in iterables]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield prod


class Expression:
    context = []
    latex_mode = False

    def __str__(self):
        pass

    def key(self):
        pass

    def contains(self, name):
        return False

    def substitute(self, values):
        pass

    def evaluate(self, values):
        pass

    def deriv(self, respect):
        pass

    def differentiate(self, respect):
        return self.deriv(respect).substitute({})

    def __add__(self, other):
        if isinstance(other, Expression):
            return Sum([self, other])
        elif isinstance(other, (int, float)):
            return Sum([self, Literal(other)])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Expression):
            return Sum([self, -other])
        elif isinstance(other, (int, float)):
            return Sum([self, Literal(-other)])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Expression):
            return Term(1, [self, other])
        elif isinstance(other, (int, float)):
            return Term(other, [self])
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Term(other, [self])
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return Power(self, Literal(other))
        return NotImplemented

    def __neg__(self):
        return Term(-1, [self])


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return format_number(self.value)

    def key(self):
        return ("literal", self.value)

    def contains(self, name):
        return False

    def substitute(self, values):
        return self

    def evaluate(self, values):
        return self.value

    def deriv(self, respect):
        return Literal(0)


class Constant(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        if Expression.latex_mode:
            return f"\\{self.name}"
        else:
            return self.name

    def key(self):
        return ("constant", self.name)

    def contains(self, name):
        return False

    def substitute(self, values):
        return self

    def evaluate(self, values):
        return self.value

    def deriv(self, respect):
        return Literal(0)


Pi = Constant("pi", math.pi)


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        if Expression.latex_mode:
            if self.name.endswith("dotdot"):
                return f"\\ddot{{{format_variable(self.name[:-6])}}}"
            elif self.name.endswith("dot"):
                return f"\\dot{{{format_variable(self.name[:-3])}}}"
        return format_variable(self.name)

    def key(self):
        return ("variiable", self.name)

    def contains(self, name):
        if name == self.name:
            return True
        elif name == "t" and self.name.replace("dot", "") in Expression.context:
            return True
        return False

    def substitute(self, values):
        if self.name in values:
            return Literal(values[self.name])
        return self

    def evaluate(self, values):
        return values[self.name]

    def deriv(self, respect):
        if self.name == respect:
            return Literal(1)
        elif respect == "t":
            return Variable(self.name + "dot")
        return Literal(0)


Var = Variable


class Power(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent

    def __str__(self):
        if Expression.latex_mode:
            if isinstance(self.base, Function):
                if self.exponent.value == 0.5:
                    base_text = str(self.base)
                    if isinstance(self.base, Sum):
                        base_text = base_text[6:-7]
                    return f"\\sqrt{{{base_text}}}"
                if isinstance(self.base.arg, Term):
                    return f"\\{self.base.name}^{{{self.exponent}}}\\left({self.base.arg}\\right)"
                return f"\\{self.base.name}^{{{self.exponent}}}{self.base.arg}"
            if isinstance(self.base, Term):
                return f"\\left({self.base}\\right)^{{{self.exponent}}}"
            return f"{self.base}^{{{self.exponent}}}"

        if isinstance(self.base, Term):
            return f"({self.base})^{self.exponent}"
        return f"{self.base}^{self.exponent}"

    def key(self):
        return ("power", self.base.key(), self.exponent.key())

    def contains(self, name):
        return self.base.contains(name) or self.exponent.contains(name)

    def substitute(self, values):
        assert isinstance(self.exponent, Literal)
        if self.exponent.value == 0:
            return Literal(1)

        if isinstance(self.base, Term):
            new_coeff = self.base.coeff ** self.exponent.value
            new_terms = [Power(term, self.exponent)
                         for term in self.base.terms]
            return Term(new_coeff, new_terms).substitute(values)

        new_base = self.base.substitute(values)
        new_exponent = self.exponent
        if isinstance(new_base, Power):
            new_exponent = Literal(
                new_base.exponent.value * new_exponent.value)
            new_base = new_base.base
        elif isinstance(new_base, Literal):
            return Literal(new_base.value ** new_exponent.value)
        if new_exponent.value == 1:
            return new_base
        return Power(new_base, new_exponent)

    def evaluate(self, values):
        return self.base.evaluate(values) ** self.exponent.evaluate(values)

    def deriv(self, respect):
        if self.base.contains(respect):
            assert isinstance(self.exponent, Literal)
            if self.exponent.value == 2:
                return Term(2, [self.base, self.base.deriv(respect)])
            return Term(self.exponent.value, [Power(self.base, Literal(self.exponent.value - 1)), self.base.deriv(respect)])
        return Literal(0)


class Term(Expression):
    def __init__(self, coeff, terms):
        assert len(terms)
        self.coeff = coeff
        self.terms = terms

    def __str__(self):
        prefix = format_number(self.coeff)
        if prefix == "-1":
            prefix = "-"
        elif prefix == "1":
            prefix = ""
        return prefix + "".join(map(str, self.terms))

    def key(self, coeff=True):
        if coeff:
            return ("term", self.coeff, tuple(sorted([term.key() for term in self.terms])))
        if len(self.terms) == 1:
            return self.terms[0].key()
        return ("term", tuple(sorted([term.key() for term in self.terms])))

    def contains(self, name):
        return any(term.contains(name) for term in self.terms)

    def substitute(self, values):
        substituted = [term.substitute(values) for term in self.terms]
        new_coeff = self.coeff
        sums = []
        keys = OrderedDict()
        for term in substituted:
            if isinstance(term, Literal):
                new_coeff *= term.value
            elif isinstance(term, Term):
                new_coeff *= term.coeff
                substituted.extend(term.terms)
            elif isinstance(term, Sum):
                sums.append(term)
            else:
                if isinstance(term, Power):
                    base = term.base
                    exp = term.exponent.value
                else:
                    base = term
                    exp = 1
                base_key = base.key()
                if base_key not in keys:
                    keys[base_key] = [base, exp]
                else:
                    keys[base_key][1] += exp

        values = list(keys.values())
        functions = [pair for pair in values if isinstance(pair[0], Function)]
        other = [pair for pair in values if not isinstance(pair[0], Function)]

        new_terms = []
        for term, exp in other + functions:
            if exp == 1:
                new_terms.append(term)
            elif exp != 0:
                new_terms.append(Power(term, Literal(exp)))

        new_terms = [term for term in new_terms if not isinstance(
            term, (Literal, Term))]
        if new_coeff == 0:
            return Literal(new_coeff)

        if sums:
            factors = [term for term in new_terms if not isinstance(term, Sum)]
            if factors:
                factors_term = Term(1, factors).substitute(values)
            else:
                factors_term = Literal(1)
            axes = [term.terms for term in sums]
            new_terms = []
            for product in cartesian_product(*axes):
                new_terms.append(
                    Term(new_coeff, [factors_term] + list(product)))
            return Sum(new_terms).substitute(values)

        if len(new_terms) == 0:
            return Literal(new_coeff)
        if new_coeff == 1 and len(new_terms) == 1:
            return new_terms[0]

        return Term(new_coeff, new_terms)

    def evaluate(self, values):
        result = self.coeff
        for term in self.terms:
            result *= term.evaluate(values)
        return result

    def deriv(self, respect):
        functions = []
        constants = []
        for term in self.terms:
            if term.contains(respect):
                functions.append(term)
            else:
                constants.append(term)
        if not functions:
            return Literal(0)
        elif len(functions) == 1:
            deriv = functions[0].deriv(respect)
        elif len(functions) == 2:
            deriv = Sum([
                Term(1, [functions[0], functions[1].deriv(respect)]),
                Term(1, [functions[1], functions[0].deriv(respect)])
            ])
        elif len(functions) > 2:
            deriv = Term(1, [functions[0], Term(
                1, functions[1:])]).deriv(respect)
        return Term(self.coeff, constants + [deriv])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Term(self.coeff * other, self.terms)
        elif isinstance(other, Term):
            return Term(self.coeff * other.coeff, self.terms + other.terms)
        elif isinstance(other, Expression):
            return Term(self.coeff, self.terms + [other])
        return NotImplemented

    def __neg__(self):
        return Term(-self.coeff, self.terms)


class Sum(Expression):
    def __init__(self, terms):
        assert len(terms)
        self.terms = terms

    def key(self):
        return ("sum", tuple(sorted([term.key() for term in self.terms])))

    def __str__(self):
        terms = " + ".join(map(str, self.terms)).replace("+ -", "- ")
        if Expression.latex_mode:
            return f"\\left({terms}\\right)"
        return f"({terms})"

    def contains(self, name):
        return any(term.contains(name) for term in self.terms)

    def substitute(self, values):
        substituted = [term.substitute(values) for term in self.terms]
        new_literal = Literal(0)
        new_terms = []
        for term in substituted:
            if isinstance(term, Literal):
                new_literal.value += term.value
            elif isinstance(term, Sum):
                substituted.extend(term.terms)
            else:
                new_terms.append(term)
        if len(new_terms) == 0:
            return new_literal

        keys = OrderedDict()
        for term in new_terms:
            term_key = term.key()
            if isinstance(term, Term):
                multiple = term.coeff
                term_key = term.key(False)
            else:
                multiple = 1
            if term_key not in keys:
                keys[term_key] = [term, multiple]
            else:
                keys[term_key][1] += multiple

        new_terms = []
        for term, coeff in keys.values():
            if coeff != 0:
                if isinstance(term, Term):
                    new_terms.append(Term(coeff, term.terms))
                elif coeff != 1:
                    new_terms.append(Term(coeff, [term]))
                else:
                    new_terms.append(term)

        if len(new_terms) == 0:
            return new_literal
        if new_literal.value == 0:
            if len(new_terms) == 1:
                return new_terms[0]
            else:
                return Sum(new_terms)
        new_terms.append(new_literal)
        return Sum(new_terms)

    def evaluate(self, values):
        result = 0
        for term in self.terms:
            result += term.evaluate(values)
        return result

    def deriv(self, respect):
        new_terms = [term.deriv(respect)
                     for term in self.terms if term.contains(respect)]
        new_terms = [term for term in new_terms if not (
            isinstance(term, Literal) and term.value == 0)]
        if not new_terms:
            return Literal(0)
        elif len(new_terms) == 1:
            return new_terms[0]
        else:
            return Sum(new_terms)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Sum(self.terms + [Literal(other)])
        elif isinstance(other, Sum):
            return Sum(self.terms + other.terms)
        elif isinstance(other, Expression):
            return Sum(self.terms + [other])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return Sum(self.terms + [Literal(-other)])
        elif isinstance(other, Expression):
            return Sum(self.terms + [-other])
        return NotImplemented


class Function(Expression):
    def __init__(self, arg, name, func, deriv_class):
        self.arg = arg
        self.name = name
        self.func = func
        self.deriv_class = deriv_class

    def __str__(self):
        if Expression.latex_mode:
            if isinstance(self.arg, Term):
                return f"\\{self.name}\\left({self.arg}\\right)"
            return f"\\{self.name}{{{self.arg}}}"

        if isinstance(self.arg, Sum):
            return f"{self.name}{self.arg}"
        return f"{self.name}({self.arg})"

    def key(self):
        return (self.name, self.arg.key())

    def contains(self, name):
        return self.arg.contains(name)

    def substitute(self, values):
        new_arg = self.arg.substitute(values)
        if isinstance(new_arg, Literal):
            return Literal(self.func(new_arg.value))
        return self.__class__(new_arg)

    def evaluate(self, values):
        return self.func(self.arg.evaluate(values))

    def deriv(self, respect):
        if self.arg.contains(respect):
            deriv = self.arg.deriv(respect)
            if isinstance(deriv, Literal) and deriv.value == 1:
                return self.deriv_class(self.arg)
            return Term(1, [self.deriv_class(self.arg), deriv])
        return Literal(0)


def negative_wrapper(cls):
    def constructor(arg):
        return -cls(arg)
    return constructor


class Sin(Function):
    def __init__(self, arg):
        super(Sin, self).__init__(arg, "sin", math.sin, Cos)

    def substitute(self, values):
        if isinstance(self.arg, Term) and self.arg.coeff < 0:
            return -Sin(Term(-self.arg.coeff, self.arg.terms)).substitute(values)
        return super(Sin, self).substitute(values)


class Cos(Function):
    def __init__(self, arg):
        super(Cos, self).__init__(arg, "cos", math.cos, negative_wrapper(Sin))

    def substitute(self, values):
        if isinstance(self.arg, Term) and self.arg.coeff < 0:
            return Cos(Term(-self.arg.coeff, self.arg.terms)).substitute(values)
        return super(Cos, self).substitute(values)
