# Mechanics

<a href="mechanics.help"><b>Mechanics</b></a> is a mechanical system simulator that uses Lagrangian mechanics and Runge-Kutta methods to simulate various constrained system. From expressions of energy, it is capable of deriving equations of motion using symbolic differentiation and then stepping through them in time to simulate the motion of the system.

# How to use

The homepage has button with images to help understand users, links to each of the system simulator pages. Each page has an energy-label and diagram, playback buttons and sometimes system equations. Mechanism metrics are present there in the right middle side. The Rolling Disk Pendulum has equations of motion too complex to display on the screen. There is also a button to view the Python system file that creates the solver. Another button, description, present there to make understand users with simple text. Under every page, there's a button says "Learn how mechmaths work", press into that button and you'll know how MechMaths, my own custom library works. The page runs best on a landscape desktop orientation.

Check out these links to find out
- <a href="mechanics.help"><b>Mechanics Homepage</b></a>
- <a href="mechanics.help/pend/"><b>Single Pendulum</b></a>
- <a href="mechanics.help/dpend/"><b>Double Pendulum</b></a>
- <a href="mechanics.help/atwood/"><b> Swinging Atwood Machine</b></a>
- <a href="mechanics.help/cart/"><b>Cart and Pendulum</b></a>
- <a href="mechanics.help/slope/"><b>Disk on Slope</b></a>
- <a href="mechanics.help/disk/"><b>Rolling Disk Pendulum</b></a>
- <a href="mechanics.help/elastic/"><b>Elastic Pendulum</b></a>
- <a href="mechanics.help/mechmaths/"><b>Learn how mechmaths work</b></a>


# Code Structure
The project is written in both Python and Javascript: the main Lagrangian system solver uses Python for its polymorphism and flexible OOP, while the renderer uses JS to efficiently draw the system and update the GUI. Minimal external dependencies are used, so almost all of the code has been written from scratch. Neither component uses nor requires the internals of the other: the system solver simply outputs a few numbers to calculate the positions of objects to draw.

# Challenges

One ofthe first major issues encountered was how to simplify expressions. Many of the basic rules in algebra are rather complicated to systematically apply, such as collecting like terms or using index laws. In fact, since the expressions obtained from the Euler-Lagrange equations are of a specific format, this symbolic differentiation engine is not fully featured.

Another detail that required significant attention was how to embed Python into a JavaScript powered webpage. The library used for this, PyScript, has two different Python interpreters: Pyodide and MicroPython, the latter of which is 37x smaller in size. The symbolic differentiation engine does not require any external dependencies. but the RK4 time stepper does use NumPy, which is not available on MicroPython. This meanth that much of the code needed to be rewritten using ulab, the MicroPython equivalent. In addition to this, many of the CPython-specific implementation details were different, such as dictionary key order and hash function limitations, had varying behaviour on MicroPython and had to be taken account of.

One of the techniques I used was dynamically creating each simulation webpage entirely using JavaScript without any frameworks such as JQuery. This meant that each simulation would have almost identical HTML and simply differing diagram drawing JS, which made adding new simulations a matter of copying the template code and editing the rendering script.

# Merits

The system code is extremely intuitive to the point where even non-programmers should be capable of understanding how the system is set-up. The most complex system, the Rolling Disk Pendulum, has no less than 7 components exerting classical forces on each other, but the Euler-Lagrange equations convert this simply to a set of simultaneous equations that can be solved instantly for individual accelerations. This results in fluid motion appearing on the screen, no matter how chaotic the system is.

# Documents
- <a href="https://github.com/imtua/mechanics/blob/main/maths/maths.md"><b>Mathematical Equations</b></a>
- <a href="https://github.com/imtua/mechanics/blob/main/mechmaths/README.md"><b>MechMaths Operations</b></a>

Simulation pages include a Parameters panel with curated physical inputs such as mass, gravity, length, radius, and spring stiffness. Every input has a model-specific safe range; changing a value clamps it to that range, rebuilds the equations, and restarts the simulation from its initial state.