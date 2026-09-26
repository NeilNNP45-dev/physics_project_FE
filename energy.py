"""Calculate the total mechanical energy of the simulated system."""

from math import hypot

from body import Body
from physics import G


def calculate_total_energy(bodies: list[Body]) -> float:
    """
    Calculate the total mechanical energy of all bodies.

    Mechanical energy has two parts:

    1. Kinetic energy
       Energy caused by an object's motion.

    2. Gravitational potential energy
       Energy caused by the gravitational interaction between objects.

    The total energy is:

        total energy = kinetic energy + potential energy
    """

    # Start by calculating the total kinetic energy.
    #
    # The kinetic energy of one body is:
    #
    #       KE = 1/2 * m * v²
    #
    # Since our velocity has two components, vx and vy:
    #
    #       v² = vx² + vy²
    #
    # We calculate this for every body and add them together.
    kinetic = sum(
        0.5 * body.mass * (body.vx * body.vx + body.vy * body.vy)
        for body in bodies
    )

    # Start the total gravitational potential energy at zero.
    potential = 0.0

    # Every pair of bodies has a gravitational interaction.
    #
    # For example:
    #
    #       Sun - Earth
    #       Sun - Mars
    #       Earth - Mars
    #
    # We only need to calculate each pair once.
    #
    # "index + 1" means that when we are looking at body A,
    # we only compare it with bodies that come after it.
    #
    # This prevents us from calculating:
    #
    #       Sun - Earth
    #       Earth - Sun
    #
    # separately, because they are the same pair.
    for index, body_a in enumerate(bodies):
        for body_b in bodies[index + 1:]:

            # Calculate the distance between the two bodies.
            #
            # hypot(dx, dy) gives:
            #
            #       sqrt(dx² + dy²)
            #
            # which is the normal 2-D distance formula.
            distance = hypot(
                body_b.x - body_a.x,
                body_b.y - body_a.y,
            )

            # If both bodies are at exactly the same position,
            # their distance would be zero.
            #
            # Dividing by zero would cause an error, so we simply
            # skip this pair.
            if distance != 0.0:

                # Gravitational potential energy between two bodies:
                #
                #       PE = -G * m1 * m2 / r
                #
                # The negative sign is important.
                # Gravitationally bound systems have negative
                # potential energy in this convention.
                potential -= (
                    G
                    * body_a.mass
                    * body_b.mass
                    / distance
                )

    # The mechanical energy of the complete system is the sum
    # of its kinetic and gravitational potential energy.
    return kinetic + potential