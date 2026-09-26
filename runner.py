from mechmaths import Expression, Solver
from pyscript import window, ffi

main_solver = None
main_initial = None

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
    window.drawSystem(ffi.to_js(main_solver.get_params()))
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


def load_solver(solver, initial, custom_steps=None, render_equations=True):
    global main_solver, main_initial, steps
    main_solver = solver
    main_initial = initial
    if custom_steps is not None:
        steps = custom_steps

    if render_equations:
        Expression.latex_mode = True
        solver2 = Solver(*solver.original)
        solver2.load_constants({})

        latex = "\\begin{align*}"
        latex += "\\\\".join(solver2.display_equations())
        latex += "\\end{align*}"
        window.setEquationlabel(latex)

        window.setPlaybackButtons(
            ffi.to_js(reset_playback),
            ffi.to_js(toggle_playback),
            ffi.to_js(step_playback)
        )
        solver.load_initial_values(initial)
        request_update()
