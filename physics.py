"""Gravity calculations and constants used by the simulation."""

from math import hypot

from body import Body


# Gravitational constant used by our simulation.
#
# This value belongs to the unit system used by the project.
G = 0.00297555


def compute_accelerations(bodies: list[Body]) -> None:
    """
    Calculate the acceleration of every body.

    Each pair of bodies is processed only once.
    """

    # Clear the old acceleration values first.
    #
    # We calculate acceleration again using the bodies'
    # current positions.
    for body in bodies:
        body.ax = 0.0
        body.ay = 0.0

    # Pick the first body in the pair.
    for index, body_a in enumerate(bodies):

        # Compare it with every body after it in the list.
        #
        # This prevents us from calculating the same pair twice.
        for body_b in bodies[index + 1:]:

            # Find the difference between the two positions.
            #
            # rx = horizontal difference
            # ry = vertical difference
            rx = body_b.x - body_a.x
            ry = body_b.y - body_a.y

            # Calculate distance squared.
            r_squared = rx * rx + ry * ry

            # If the bodies are at exactly the same position,
            # there is no useful direction to calculate.
            if r_squared == 0.0:
                continue

            # Calculate the actual distance between the bodies.
            distance = hypot(rx, ry)

            # Calculate how strongly body_b affects body_a.
            factor_a = (
                G
                * body_b.mass
                / (r_squared * distance)
            )

            # Calculate how strongly body_a affects body_b.
            factor_b = (
                G
                * body_a.mass
                / (r_squared * distance)
            )

            # Add body_b's acceleration to body_a.
            body_a.ax += factor_a * rx
            body_a.ay += factor_a * ry

            # Add body_a's acceleration to body_b.
            #
            # The minus sign makes the acceleration point
            # in the opposite direction.
            body_b.ax -= factor_b * rx
            body_b.ay -= factor_b * ry