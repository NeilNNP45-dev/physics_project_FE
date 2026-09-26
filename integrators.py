"""Numerical integration methods used to move the bodies."""


from body import Body
from physics import compute_accelerations


def euler_step(bodies: list[Body], dt: float) -> None:
    """
    Move all bodies forward by one time step using Euler integration.

    The function:
    1. Calculates the current acceleration of every body.
    2. Updates each body's position.
    3. Updates each body's velocity.
    4. Updates each body's trail.
    """

    # Calculate the gravitational acceleration of every body
    # before changing any positions or velocities.
    compute_accelerations(bodies)

    for body in bodies:

        # Save the current velocity before changing it.
        #
        # We use this old velocity for the position update.
        old_vx = body.vx
        old_vy = body.vy

        # Update the body's position.
        body.x += old_vx * dt
        body.y += old_vy * dt

        # Update the body's velocity using its acceleration.
        body.vx += body.ax * dt
        body.vy += body.ay * dt

        # Store the body's new position for its visible trail.
        body.update_trail()


def velocity_verlet_step(bodies: list[Body], dt: float) -> None:
    """
    Move all bodies forward by one time step using Velocity Verlet.

    Unlike the Euler step, this method needs the acceleration
    both before and after the position update.
    """

    # Calculate the acceleration at the beginning of the time step.
    compute_accelerations(bodies)

    # Save the current acceleration of every body.
    #
    # We need these values later, after the positions have changed.
    previous_accelerations = [
        (body.ax, body.ay)
        for body in bodies
    ]

    # Update the positions using the current velocity
    # and the acceleration we just calculated.
    #
    # zip() lets us work with each body and its saved acceleration
    # at the same time.
    for body, (old_ax, old_ay) in zip(
        bodies,
        previous_accelerations,
    ):
        body.x += (
            body.vx * dt
            + 0.5 * old_ax * dt * dt
        )

        body.y += (
            body.vy * dt
            + 0.5 * old_ay * dt * dt
        )

    # The bodies have moved, so their gravitational accelerations
    # may have changed.
    #
    # Calculate the new accelerations at their new positions.
    compute_accelerations(bodies)

    # Update the velocities using both the old and new accelerations.
    for body, (old_ax, old_ay) in zip(
        bodies,
        previous_accelerations,
    ):
        body.vx += 0.5 * (old_ax + body.ax) * dt
        body.vy += 0.5 * (old_ay + body.ay) * dt

        # Store the body's new position for its visible trail.
        body.update_trail()