# Research and Physical Model

## 1. Introduction

This project is a two-dimensional Solar-System orbit simulator based on
Newtonian gravity and numerical integration.

The purpose of the project is to study how celestial bodies move under
gravitational forces and how numerical methods can be used to calculate
their motion over time.

The simulation contains the Sun and the eight major planets. Additional
small bodies can also be introduced to study gravitational perturbations.

The model is designed to be physically grounded while remaining simple
enough to understand and run as a first-year computational physics project.


# 2. Project Objective

The main objectives of the simulation are:

- Model gravitational interaction between multiple celestial bodies.
- Use researched masses and initial states for the Solar System.
- Calculate the resulting accelerations using Newtonian gravity.
- Use numerical integration to update positions and velocities.
- Compare different numerical integration methods.
- Monitor the total mechanical energy of the system.
- Provide a visual representation of the resulting motion.
- Allow additional bodies to be introduced for controlled experiments.

The simulation is not intended to reproduce every physical effect present
in the real Solar System.

Instead, it uses a simplified physical model that focuses on Newtonian
gravitational dynamics.


# 3. Model Overview

The simulation uses an **N-body model**.

In an N-body system, every body can exert a gravitational force on every
other body.

For example, the Earth is affected by:

- the Sun
- the Moon, if it were included
- other planets
- any additional bodies in the simulation

The current model does not include every real celestial object. It focuses
on the Sun and the eight planets, with optional additional bodies.

The system is simulated in two spatial dimensions:

```text
             +Y
              |
              |
              |
              +------------ +X
```

Each body therefore has:

- position: `x`, `y`
- velocity: `vx`, `vy`
- acceleration: `ax`, `ay`


# 4. Unit System

Using SI units directly would result in extremely large and inconvenient
numbers for planetary simulation.

For example, planetary distances are measured in hundreds of millions of
kilometres and planetary masses are measured in extremely large numbers
of kilograms.

Therefore, the simulation uses a scaled unit system.

| Quantity | Simulation Unit |
|---|---|
| Distance | million kilometres |
| Mass | Earth masses |
| Time | days |
| Velocity | million kilometres/day |
| Acceleration | million kilometres/day² |

## 4.1 Distance

One simulation distance unit represents:

```text
1 unit = 1 million kilometres
```

Therefore:

```text
Earth-Sun distance ≈ 150
```

corresponds to approximately:

```text
150 million kilometres
```


## 4.2 Mass

Mass is measured relative to the mass of Earth.

Therefore:

```text
Earth mass = 1
```

The Sun has a mass of approximately:

```text
Sun mass = 332946.05 Earth masses
```

This makes the relative masses of the planets much easier to work with.


## 4.3 Time

Time is measured in days.

Therefore:

```text
1 simulation time unit = 1 day
```


## 4.4 Velocity

Velocity is therefore measured in:

```text
million kilometres/day
```

For example:

```text
vx = 1
```

means that the body has an x-direction velocity of one million
kilometres per day.


## 4.5 Acceleration

Acceleration is measured in:

```text
million kilometres/day²
```

This is the change in velocity per simulation day.


# 5. Gravitational Constant

The simulation uses:

```text
G = 0.00297555
```

This is not the numerical value of the gravitational constant when written
in SI units.

Instead, it is the value of the gravitational constant after converting
it to the unit system used by this simulation.

The resulting units are:

```text
million kilometres³
-------------------
Earth mass × day²
```

Using this value allows Newton's law of universal gravitation to work
directly with the simulation's scaled distances, masses, and times.


# 6. Newtonian Gravity

The simulation is based on Newton's law of universal gravitation.

For two bodies with masses `m₁` and `m₂`, separated by a distance `r`:

$
F = G\frac{m_1m_2}{r^2}
$

where:

- `F` is gravitational force
- `G` is the gravitational constant
- `m₁` and `m₂` are the two masses
- `r` is the distance between their centres

Gravity is always attractive.


## 6.1 From Force to Acceleration

Newton's second law states:

$
F = ma
$

where:

Therefore, the acceleration of body 1 caused by body 2 can be written as:

$
a_1 = G\frac{m_2}{r^2}
$

In two dimensions, the direction of the acceleration must also be
considered.

Let:

$
r_x = x_2-x_1
$

and:

$
r_y = y_2-y_1
$

The distance is:

$
r = \sqrt{r_x^2+r_y^2}
$

The acceleration components are then:

$
a_x =
G\frac{m_2r_x}{r^3}
$

$
a_y =
G\frac{m_2r_y}{r^3}
$

These are the equations implemented in `physics.py`.


# 7. N-Body Gravity Calculation

The simulation contains multiple bodies, so the acceleration of each body
is the combined effect of all the other bodies.

For each pair of bodies:

```text
Body A ← gravitational effect of Body B
Body B ← gravitational effect of Body A
```

The program processes each pair only once.

For example, if there are three bodies:

```text
A
B
C
```

the required pairs are:

```text
A-B
A-C
B-C
```

The simulation does not separately calculate:

```text
A-B
B-A
```

because those two calculations describe the same interaction.

This reduces unnecessary work while preserving the gravitational effects on
both bodies.


# 8. Initial Solar-System State

The initial positions and velocities of the Solar-System bodies are based
on researched orbital parameters.

The model uses:

- semi-major axis
- orbital eccentricity
- true anomaly
- Solar gravitational parameter

to determine the initial orbital state.

The resulting state is then represented using Cartesian coordinates:

```text
(x, y)
(vx, vy)
```

rather than continuously calculating orbital elements during the
simulation.

This allows the simulation to evolve naturally according to the
gravitational interactions between the bodies.


# 9. Orbital Parameters

For an orbit with semi-major axis `a` and eccentricity `e`, the orbital
parameter is:

$
p=a(1-e^2)
$

The distance from the central body at a given true anomaly `ν` is:

$
r=\frac{a(1-e^2)}
        {1+e\cos(\nu)}
$

The radial and tangential components of velocity are:

$
v_r=
\sqrt{\frac{\mu}{p}}e\sin(\nu)
$

and:

$
v_t=
\sqrt{\frac{\mu}{p}}
(1+e\cos(\nu))
$

where:

$
\mu = GM
$

For the Solar System model:

```text
μ ≈ 990.70
```

in the simulation's unit system.

These orbital equations are used to obtain physically meaningful initial
conditions before the numerical simulation begins.


# 10. Centre-of-Mass Correction

A real Solar System does not have the Sun perfectly fixed at the origin.

Every body exerts a gravitational force on every other body, including the
planets acting on the Sun.

The initial state therefore includes a centre-of-mass correction so that
the complete system has a consistent overall motion.

This is important because otherwise the chosen coordinate system can
introduce an artificial drift into the simulation.

The simulation still uses the Sun as the main visual reference, but the
physics allows the Sun to respond to the other bodies.


# 11. Numerical Integration

The equations of motion tell us the acceleration of each body.

However, acceleration alone does not directly give us the new position
and velocity after every small time interval.

A numerical integration method is therefore required.

The project currently includes two methods:

1. Euler integration
2. Velocity Verlet integration


# 12. Euler Integration

Euler integration is one of the simplest numerical integration methods.

For a small time step `Δt`:

$
x_{new}=x_{old}+v_x\Delta t
$

$
y_{new}=y_{old}+v_y\Delta t
$

The velocity is updated using acceleration:

$
v_{x,new}=v_{x,old}+a_x\Delta t
$

$
v_{y,new}=v_{y,old}+a_y\Delta t
$

Euler integration is simple and easy to understand.

However, it can accumulate numerical error relatively quickly, especially
during long-running orbital simulations.

This makes it useful in this project as both:

- a simple introduction to numerical integration
- a comparison method against Velocity Verlet


# 13. Velocity Verlet Integration

Velocity Verlet is a numerical integration method that is well suited to
many mechanical systems.

The position is first updated using the current velocity and acceleration:

$$
x_{new}
=
x_{old}
+
v_x\Delta t
+
\frac{1}{2}a_x\Delta t^2
$$

$$
y_{new}
=
y_{old}
+
v_y\Delta t
+
\frac{1}{2}a_y\Delta t^2
$$

The accelerations are then recalculated using the new positions.

Finally, the velocity is updated using the average of the old and new
accelerations:

$$
v_{x,new}
=
v_{x,old}
+
\frac{1}{2}
(a_{x,old}+a_{x,new})\Delta t
$$

$$
v_{y,new}
=
v_{y,old}
+
\frac{1}{2}
(a_{y,old}+a_{y,new})\Delta t
$$

The implementation therefore calculates gravitational acceleration twice
during one Velocity Verlet step.

This is more computationally expensive than a basic Euler step, but it
generally provides better behaviour for orbital simulations.


# 14. Comparing the Integrators

Both integrators solve the same physical problem.

The difference is how they approximate the continuous motion.

| Property | Euler | Velocity Verlet |
|---|---|---|
| Simplicity | Very simple | More involved |
| Acceleration calculations | 1 per step | 2 per step |
| Numerical accuracy | Lower | Generally higher |
| Long-term orbital behaviour | More error-prone | Better suited to orbital motion |
| Purpose in project | Basic comparison | Main integration method |

The simulation allows the user to switch between the two methods.

This makes the numerical behaviour directly observable.


# 15. Mechanical Energy

The simulation also calculates the total mechanical energy of the system.

Mechanical energy is the sum of kinetic and gravitational potential energy.

$
E = K + U
$


## 15.1 Kinetic Energy

For a body with mass `m` and speed `v`:

$
K=\frac{1}{2}mv^2
$

Since velocity has two components:

$
v^2=v_x^2+v_y^2
$

Therefore:

$
K=
\frac{1}{2}m(v_x^2+v_y^2)
$


## 15.2 Gravitational Potential Energy

For two bodies:

$
U=-G\frac{m_1m_2}{r}
$

The negative sign represents the fact that gravity is an attractive force.

The total potential energy of the system is calculated by summing the
potential energy of every unique pair of bodies.


## 15.3 Why Monitor Energy?

In an ideal isolated physical system, total mechanical energy is conserved.

A numerical simulation is only an approximation of the continuous physical
system, so small numerical errors can occur.

Monitoring the total energy therefore gives us a useful diagnostic.

It helps us observe how the numerical integration method behaves over time.

Energy should not be expected to remain perfectly constant in every
numerical calculation.


# 16. Additional Bodies and Asteroids

The simulation allows the user to add additional bodies during runtime.

These bodies are intended for experimentation with gravitational
perturbations.

Their initial conditions can include:

- position
- velocity
- mass
- visual radius
- colour

The initial velocity is not automatically calculated to place the body into
a circular orbit.

Instead, the body receives explicit initial conditions and is then allowed
to evolve naturally under the gravitational forces in the simulation.

This makes the additional bodies useful for studying how different initial
conditions affect motion.


## 16.1 Asteroid Masses

Asteroid masses are kept within physically plausible scales rather than
being artificially increased simply to make their gravitational effects
obvious.

The real asteroid population contains an extremely large range of masses.

The simulation does not attempt to reproduce the complete asteroid belt.

Instead, additional bodies are used as simplified experimental objects.

A very massive object should therefore not be interpreted as an ordinary
asteroid unless its mass is within an appropriate physical range.


## 16.2 Asteroid Radius

The displayed radius of an additional body is primarily a visual
representation.

The gravitational calculation depends on the body's mass and position,
not on its displayed radius.

Therefore, the current model does not attempt to calculate asteroid
diameter from mass and density.

A physically complete asteroid model would require assumptions about:

- density
- composition
- shape
- mass
- physical radius

Those details are outside the scope of the current project.


# 17. Collisions

Collision dynamics are currently outside the scope of the model.

Bodies can therefore pass through one another visually while continuing to
interact gravitationally.

This is a deliberate modelling decision.

Adding collisions would require additional physical assumptions.

For example, after a collision we would need to decide whether the bodies:

- merge
- bounce
- fragment
- lose kinetic energy
- conserve momentum
- conserve energy

A realistic collision and fragmentation model would therefore introduce
another significant area of physics.

The current project focuses on gravitational N-body dynamics rather than
collision dynamics.


# 18. Assumptions and Limitations

The simulation intentionally simplifies several aspects of the real Solar
System.

### Included

- Newtonian gravity
- N-body gravitational interaction
- Sun and eight planets
- Research-based initial conditions
- Two-dimensional motion
- Euler integration
- Velocity Verlet integration
- Mechanical energy calculation
- Additional experimental bodies

### Not currently included

- Three-dimensional orbital inclinations
- The Moon
- Complete asteroid-belt population
- Dwarf planets as separate simulated bodies
- Comets
- Relativistic corrections
- Solar radiation pressure
- Non-gravitational forces
- Atmospheric effects
- Physical collision dynamics
- Collision fragmentation
- Detailed asteroid density and composition

These limitations do not mean that the simulation is incorrect.

They define the scope of the model.

A useful scientific model does not need to include every physical effect.
It needs to clearly state which effects are included and which are
ignored.


# 19. Code-to-Physics Mapping

The project separates the physical model from the visualisation and user
interface.

```text
                    Solar-System State
                           |
                           v
                       body.py
                           |
                           v
                      physics.py
                  Calculate gravity
                           |
                           v
                    integrators.py
                Update positions/velocity
                           |
                           v
                       energy.py
                 Calculate total energy
                           |
                           v
                      renderer.py
                   Display the system
                           ^
                           |
                      camera.py
                World ↔ screen coordinates
```

## `body.py`

Represents individual physical bodies.

It stores:

- mass
- radius
- position
- velocity
- acceleration
- colour
- trail information

It also contains the initial Solar-System configuration.


## `physics.py`

Contains the gravitational model.

Its main responsibility is calculating the acceleration of every body
caused by every other body.

The gravitational constant `G` is also defined here.


## `integrators.py`

Contains the numerical integration methods.

The current methods are:

- `euler_step()`
- `velocity_verlet_step()`

These functions use the accelerations calculated by `physics.py` to move
the bodies forward in time.


## `energy.py`

Calculates the total mechanical energy of the system.

It contains:

- kinetic energy
- gravitational potential energy
- total energy

This is used as a diagnostic for the numerical simulation.


## `camera.py`

Handles the conversion between physical world coordinates and screen
coordinates.

It also controls:

- camera movement
- zoom
- camera reset

The camera does not affect the physical simulation.

It only changes how the simulation is viewed.


## `renderer.py`

Handles visualisation.

It draws:

- background
- stars
- bodies
- orbital trails
- HUD information
- notifications

The renderer does not calculate gravitational forces or modify the physical
state of the simulation.


## `main.py`

Acts as the main controller of the program.

It:

- starts Pygame
- creates the Solar-System bodies
- runs the simulation loop
- handles keyboard and mouse input
- selects the numerical integrator
- controls simulation speed
- spawns additional bodies
- requests energy calculations
- sends the current state to the renderer


# 20. Computational Considerations

The gravitational calculation checks every unique pair of bodies.

For `N` bodies, the number of unique pairs is:

$
\frac{N(N-1)}{2}
$

Therefore, the gravitational calculation has approximately:

$
O(N^2)
$

time complexity.

For the small number of bodies used in this project, this is practical
and keeps the implementation simple and easy to understand.

More advanced simulations with thousands or millions of bodies would require
more advanced techniques such as spatial partitioning or approximate
gravity algorithms.

Those techniques are outside the scope of this project.


# 21. Conclusion

This project demonstrates how a physical system can be represented using
mathematical equations and then approximated computationally.

The main process is:

```text
Physical laws
      ↓
Mathematical equations
      ↓
Numerical integration
      ↓
Computer simulation
      ↓
Visualisation and analysis
```

The simulation uses Newtonian gravity to determine the accelerations of
celestial bodies and numerical integration to calculate their motion over
time.

The project deliberately uses a simplified model so that the underlying
physics and computational methods remain understandable.

The goal is therefore not to create a perfect copy of the real Solar
System, but to build a physically meaningful computational model that can
be studied, tested, and extended.
