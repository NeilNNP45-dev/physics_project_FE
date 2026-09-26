# Academic Solar-System Orbit Simulator

A readable first-year Physics project that simulates a two-dimensional Solar System using Newtonian N-body gravity and numerical integration.

The simulator includes the Sun, eight planets, Euler integration, Velocity Verlet integration, orbital trails, camera controls, total-energy diagnostics, and interactive asteroid spawning.

## Project Scope

This project is designed as an educational computational-physics model. It uses physically motivated Solar-System parameters and researched initial conditions while deliberately simplifying the real Solar System so that the underlying physics and numerical methods remain understandable.

The project focuses on:

- Newtonian gravitational interaction
- N-body simulation
- Numerical integration
- Conservation of mechanical energy
- Visualization of orbital motion
- Comparing Euler and Velocity Verlet integration

## Run

This project uses a Python virtual environment so that its dependencies are isolated from the system Python installation.

### 1. Create a virtual environment

Make sure Python 3.13 is installed, then run:

```bash
py -3.13 -m venv .venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the simulator

```bash
python main.py
```

When the virtual environment is active, `python` refers to the Python version inside `.venv` rather than the system-wide Python installation.

> **Note:** If PowerShell blocks the activation script, the project can still be run by using the Python executable inside `.venv` directly, or by activating the environment through another terminal.

The simulation uses million kilometres, Earth masses, days, million kilometres/day, and million kilometres/day².

The gravitational constant and Solar-System initial values are adapted from the author's personal [COSMOS project](https://github.com/NeilNNP45-dev/COSMOS). This repository is a separate academic derivative. It does not contain the COSMOS architecture and does not modify COSMOS.

## Controls

| Control | Action |
| --- | --- |
| `W/A/S/D` | Pan camera |
| `I/O` | Zoom in/out |
| `Space` | Pause/resume |
| `R` | Reset Solar System |
| `E` | Switch Euler/Velocity Verlet |
| `Up/Down` | Change time scale |
| `M` / `N` | Use 80× / 1× time scale |
| Left click | Spawn asteroid |

Asteroids are given explicit initial positions, velocities, masses, and radii. Their motion is then determined by the same N-body gravitational model as the rest of the simulation.

## Physical Model

The simulation uses Newtonian gravity in two dimensions. Each body interacts gravitationally with every other body in the system.

The initial Solar-System state is based on researched orbital parameters and a centre-of-mass correction. The resulting Cartesian positions and velocities are stored directly in the simulation.

Two numerical integration methods are available:

- **Euler:** simple first-order integration that is easy to understand but can accumulate significant numerical error.
- **Velocity Verlet:** a more accurate and stable method for orbital simulations, with better long-term energy behaviour under suitable conditions.

The simulator also calculates the system's total mechanical energy as a diagnostic for studying numerical behaviour.

See [`research.md`](research.md) for the equations, units, assumptions, initialization method, numerical methods and limitations.

## Limitations

This is a simplified 2-D Newtonian educational model. It does not attempt to reproduce every physical effect present in the real Solar System.

The current model omits:

- Collision and fragmentation dynamics
- Three-dimensional orbital inclinations
- The Moon
- Asteroid-belt and other minor-body populations
- Comets and dwarf planets
- Relativistic corrections
- Radiation pressure and other non-gravitational forces
- Exact historical ephemeris state vectors

These limitations are intentional and define the current scope of the project.

## Developer Note

> 🪐 **Built with curiosity, persistence, and an unreasonable interest in making planets go around in circles.**
>
> This project was developed as a first-year Physics academic project by **Neil N. P.** while exploring computational physics, Python, and numerical simulation.
>
> The project is also an opportunity to explore ideas from **[COSMOS](https://github.com/NeilNNP45-dev/COSMOS)**, a separate personal space-simulation project.
>
> **Building one star at a time.** ✨
>
> *Keep learning. Keep building. Keep asking why.*
