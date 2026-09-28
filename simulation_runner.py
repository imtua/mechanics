import ujson as json

from mechmaths import Expression, Solver
from pyscript import window, ffi

main_solver = None
main_initial = None
main_constants = None
main_parameters = None

steps = 20
dt = 1/60
last = 0
paused = False


def update(timestamp):
    global last
    progress = min(timestamp / 1000 - last, dt + 1e-6)
    last = timestamp / 1000

    while progress > dt / steps:
        progress -= dt / steps
        main_solver.step(dt / steps)
    update_screen()

    if not paused:
        request_update()


def update_screen():
    params = main_solver.get_params()
    window.drawSystem(ffi.to_js(params))
    window.setMetrics(
        main_solver.time,
        ffi.to_js(params),
        ffi.to_js(main_solver.phase[1].tolist())
    )
    t, v = main_solver.get_energies()
    window.setEnergyLabel(t, v)


def request_update():
    window.requestAnimationFrame(ffi.to_js(update))


def toggle_playback():
    global paused
    paused = not paused
    if not paused:
        request_update()
    return paused


def step_playback():
    global paused
    paused = True
    request_update()


def reset_playback():
    global paused
    main_solver.load_initial_values(main_initial)
    paused = True
    update_screen()

def render_equation_label():
    Expression.latex_mode = True
    solver2 = Solver(*main_solver.original)
    solver2.load_constants({})
    latex = "\\begin{align*}"
    latex += "\\\\".join(solver2.display_equations())
    latex += "\\end{align*}"
    window.setEquationlabel(latex)

def update_parameters(values):
    constants = main_constants.copy()
    for i, parameter in enumerate(main_parameters):
        value = float(values[i])
        value = max(parameter["min"], min(parameter["max"], value))
        constants[parameter["name"]] = value
    main_solver.load_constants(constants)
    main_solver.load_initial_values(main_initial)
    render_equation_label()
    update_screen()


def load_solver(solver, initial, custom_steps=None, render_equations=True,
                constants=None, parameters=None):
    global main_solver, main_initial, main_constants, main_parameters, steps
    main_solver = solver
    main_initial = initial
    main_constants = constants
    main_parameters = parameters
    if custom_steps is not None:
        steps = custom_steps

    if render_equations:
        render_equation_label()
        window.setPlaybackButtons(
            ffi.to_js(reset_playback),
            ffi.to_js(toggle_playback),
            ffi.to_js(step_playback)
        )
    window.applySimulationParameters = ffi.to_js(update_parameters)
    if main_parameters is not None:
        window.setParameterControls(
            json.dumps(main_parameters),
            json.dumps(main_constants)
        )
    solver.load_initial_values(initial)
    request_update()
