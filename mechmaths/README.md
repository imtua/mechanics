# Mechmaths

**Mechmaths**, meaning mechanics and mathematics, is a small symbolic mechanics and numerical simulation library that includes 6 of the most misunderstood mechanics. It turns a discription of a mechanical system into equations of motion and then integrates those equation over time.

## Overall Pipeline
First, the mechanical system's kinematics are defined using generalized coordinate position expressions, which are used to formulate kinetic ($T$) and potential ($V$) energy. These yield the lagrangian, $L = T - V$. Applying the Euler-Lagrange equations produces the equations of motion in matrix form, $M(q,\dot{q})\ddot{q} = b(q, \dot{q})$. Finally, a linear solver computes the generalized accelerations ($\ddot{q}$), which are then integrated forward in time using a fourth-order Runge-Kutta (RK4) scheme.

## Package Layout

### `__init__.py`

`__init__.py` is the public entry point that re-exports:
- **Expression**, the base class for symbolic expressions.
- **Var**. an alias for Variable.
- **Pi**, a symbolic constant containing 'math.pi'.
- **Solver**, the numerical simulation class.

The lower-class classes can still be imported directly from **deriv** and **system**.

### `deriv.py`

`deriv.py` is the module that implements the symbolic  expression tree. It does not use a general purpose computer algebra package. Instead, every expression is represented by one of the library's Python classes, and each class knows how to print, substitute, evaluate, simplify, and differentiate itself.

### `system.py`

`system.py` is the module that provides mechanical building blocks. Components create symbolic positions and energy expressions using **Vector** objects. **System** gathers the component energies into total kinetic and potential energy.

### `engine.py`

`engine.py` is the module that converts a Lagrangian into equations of motion and numerically solves them. It supports both normal NumPy and the smaller **ulab** libraries, which makes the same engine usable on MicroPython-capable hardware.

## The symbolic expression system

This library builds symbolic Lagrangian mechanics models and integrates their motion numerically. At its core is an Expression tree (Literal, Constant, Variable, Sum, Term, Power, and trig functions) supporting string/LaTeX display, differentiation, substitution, and evaluation. Simplification rules flatten and combine terms, while a structural key() function canonicalizes expressions so equivalent terms (like $x+y$ and $y+x$) merge correctly. On top of this, system.py models mechanical components such as Vector, Mass, Spring, and Disk, each computing kinetic and potential energy from constrained positions (hinges, planes, circles), which a duck-typed system class aggregates. engine.py then derives equations of motion via the Euler-Lagrange equation, assembling a linear system $M(q,\dot{q})\ddot{q} + c(q, \dot{q}) = 0$ by isolating acceleration-term coefficients. This is solved numerically (via NumPy or a MicroPython-compatible Cholesky fallback) and integrated forward in time using classical fourth-order Runge-Kutta. Together, the pieces form a pipeline: define coordinates and components, derive symbolic equations of motion automaticallym, then simulate the system's dynamics step by step.

## Why this design is useful

The library separates model construction from solving. A user describes geometry and energies with ordinary Python operators, while the expression tree performs differentiation and simplification automatically. The same symbolic model can then be displayed as equations, evaluated numerically, or sent through the NumPy/MicroPython numerical backend. This keeps the mechanics code compact and makes the generated equations inspectable before simulation.
