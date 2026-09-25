from mechmaths.deriv import Var, Sin, Cos, Literal, Expression, Sum


def conv(value):
    if isinstance(value, (float, int)):
        return Literal(value)
    return value


class Vector:
    def __init__(self, x, y):
        self.x = conv(x)
        self.y = conv(y)

    def differentiate(self, respect):
        return Vector(
            self.x.differentiate(respect),
            self.y.differentiate(respect)
        )

    def mag_squared(self):
        return self.x ** 2 + self.y ** 2

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        other = conv(other)
        if isinstance(other, Expression):
            return Vector(self.x * other, self.y * other)
        return NotImplemented

    def rotate(self, angle):
        x = self.x * Cos(angle) + self.y * Sin(angle)
        y = self.x * -Sin(angle) + self.y * Cos(angle)
        return Vector(x, y)

    @staticmethod
    def polar(r, theta):
        x = conv(r) * Sin(conv(theta))
        y = -conv(r) * Cos(conv(theta))
        return Vector(x, y)


class Mass:
    def __init__(self, name):
        self.mass_var = Var(name)
        self.position = None

    def constrain_hinge(self, name, offset, center=None, ccw=True):
        if ccw:
            axis = offset.rotate(-Var(name))
        else:
            axis = offset.rotate(Var(name))
        if center is None:
            self.position = axis
        else:
            self.position = center + axis

    def constrain_plane(self, name, plane, offset=None):
        if offset:
            self.position = offset + plane * Var(name)
        else:
            self.position = plane * Var(name)

    def kinetic(self):
        velocity = self.position.differentiate("t")
        return 0.5 * self.mass_var * velocity.mag_squared()

    def potential(self):
        return self.mass_var * Var("g") * self.position.y


class Spring:
    def __init__(self, point1, point2, length, stiffness):
        self.point1 = point1
        self.point2 = point2
        self.length = conv(length)
        self.stiffness = conv(stiffness)

    def potential(self):
        distance2 = (self.point2 - self.point1).mag_squared()
        extension = distance2 ** 0.5 - self.length
        return 0.5 * self.stiffness * extension ** 2


class Disk:
    def __init__(self, mass, inertia, radius, com=None):
        self.mass_var = Var(mass)
        self.inertia_var = Var(inertia)
        self.radius = conv(radius)
        self.com = com
        self.position = None
        self.rotation = None

    def local(self, point):
        return self.position + point.rotate(self.rotation)

    def set_com_position(self):
        if self.com is not None:
            self.com_position = self.local(self.com)
        else:
            self.com_position = self.position

    def constrain_plane(self, name, plane, offset=None):
        length_inv = plane.mag_squared() ** -0.5
        plane = plane * length_inv
        normal = Vector(-plane.y, plane.x)
        self.position = normal * self.radius + plane * Var(name)
        self.rotation = Var(name) * self.radius ** -1
        if offset is not None:
            self.position = offset + self.position
        self.set_com_position()

    def constrain_circle(self, name, center, radius, circle_rotation=None):
        if circle_rotation is None:
            circle_rotation = Literal(0)
        radius = conv(radius)
        movement_radius = radius - self.radius
        self.position = center + Vector(0, -movement_radius).rotate(-Var(name))
        angle = circle_rotation - (-Var(name))
        self.rotation = circle_rotation + angle * movement_radius * self.radius ** -1
        self.set_com_position()

    def kinetic(self):
        velocity = self.com_position.differentiate("t")
        linear = 0.5 * self.mass_var * velocity.mag_squared()
        angular_vel = self.rotation.differentiate("t")
        angular = 0.5 * self.inertia_var * angular_vel ** 2
        return linear + angular

    def potential(self):
        return self.mass_var * Var("g") * self.com_position.y


class System:
    def __init__(self, *components):
        self.kinetics = []
        self.potentials = []
        for component in components:
            if hasattr(component, "kinetic"):
                self.kinetics.append(component)
            if hasattr(component, "potential"):
                self.potentials.append(component)

    def kinetic(self):
        return Sum([compoent.kinetic() for compoent in self.kinetics])

    def potential(self):
        return Sum([compoent.potential() for compoent in self.potentials])
