# Academic Solar-System Orbit Simulator

A readable first-year Physics project that simulates a two-dimensional Solar System with Newtonian N-body gravity.

The simulator includes the Sun, eight planets, Euler integration, Velocity Verlet integration, trails, camera controls, total-energy diagnostics, and interactive asteroid spawning.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

The simulation uses million kilometres, Earth masses, days, million kilometres/day, and million kilometres/day². Its gravitational constant and Solar-System initial values are adapted from the author's personal [COSMOS project](https://github.com/NeilNNP45-dev/COSMOS). This repository is a separate academic derivative; it does not contain the COSMOS architecture and does not modify COSMOS.

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

## Limitations

This is a 2-D Newtonian educational model. It omits collisions, 3-D inclination, the Moon, minor bodies, relativistic corrections, and exact historical state vectors. See [physics.md](physics.md) for the equations, assumptions, initialization method, and Euler/Velocity Verlet comparison.
