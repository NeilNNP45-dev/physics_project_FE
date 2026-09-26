"""Physical bodies and the starting state of our Solar System."""

from math import hypot


class Body:
    """
    Represents one object in our simulation.

    A body can be a planet, the Sun, or an asteroid.

    We store its:
    - physical properties, like mass and radius
    - position, using x and y
    - velocity, using vx and vy
    - acceleration, using ax and ay
    - colour, so we know how to draw it
    - trail, so we can see its path
    """

    def __init__(
        self,
        name: str,
        mass: float,
        radius: float,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: tuple[int, int, int],
    ) -> None:
        # Basic information about the body.
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color

        # Position of the body.
        # x and y tell us where the body is in the simulation.
        self.x = x
        self.y = y

        # Velocity of the body.
        # vx is velocity in the x direction.
        # vy is velocity in the y direction.
        self.vx = vx
        self.vy = vy

        # Acceleration tells us how the velocity changes.
        #
        # These start at zero because the physics system will
        # calculate the actual gravitational acceleration later.
        self.ax = 0.0
        self.ay = 0.0

        # The trail stores previous positions of the body.
        #
        # Each point is stored as:
        # (x position, y position)
        #
        # We create a new empty list for every body.
        # This is important because every body needs its own trail.
        self.trail: list[tuple[float, float]] = []

        # The minimum physical distance the body must travel
        # before another point is added to its trail.
        #
        # This prevents us from storing thousands of almost-identical
        # points when the body moves only a tiny amount.
        self.trail_spacing = 0.1

        # Maximum physical length of the visible trail.
        #
        # Once the trail becomes longer than this, the oldest
        # points are removed.
        self.max_trail_distance = 100.0

        # Keeps track of the total physical length of the trail.
        #
        # We use this so we know when old trail points should be removed.
        self.trail_distance = 0.0

    @property
    def speed(self) -> float:
        """
        Return the body's current speed.

        Velocity has two components:
        - vx in the x direction
        - vy in the y direction

        Using Pythagoras:

            speed = sqrt(vx² + vy²)

        hypot() performs this calculation for us.
        """
        return hypot(self.vx, self.vy)

    def update_trail(self) -> None:
        """Store points along the body's path while keeping the trail finite."""

        # If there are no points yet, store the body's current position
        # as the first point in the trail.
        if not self.trail:
            self.trail.append((self.x, self.y))
            return

        # Get the position of the most recently stored trail point.
        last_x, last_y = self.trail[-1]

        # Calculate how far the body has moved since that point.
        #
        # Again, this is just the distance formula:
        #
        # distance = sqrt((x2 - x1)² + (y2 - y1)²)
        distance = hypot(self.x - last_x, self.y - last_y)

        # If the body has not moved far enough, we don't need
        # another trail point yet.
        if distance < self.trail_spacing:
            return

        # The body has moved far enough, so store its new position.
        self.trail.append((self.x, self.y))

        # Add the new section of trail to our total trail length.
        self.trail_distance += distance

        # If the trail has become too long, remove the oldest points.
        #
        # We keep doing this until the trail is within the allowed
        # maximum length.
        while len(self.trail) > 1 and self.trail_distance > self.max_trail_distance:
            # Get the first two points in the trail.
            first_x, first_y = self.trail[0]
            second_x, second_y = self.trail[1]

            # The distance between these two points is the piece
            # of trail that we are about to remove.
            self.trail_distance -= hypot(
                second_x - first_x,
                second_y - first_y,
            )

            # Remove the oldest point.
            self.trail.pop(0)

    def clear_trail(self) -> None:
        """Remove all stored trail points."""

        # Empty the list of trail points.
        self.trail.clear()

        # The trail has no length anymore.
        self.trail_distance = 0.0


def create_solar_system() -> list[Body]:
    """
    Create the starting Solar System used by the simulation.

    The positions and velocities below come from the researched
    Solar System state used for this project.

    The simulation uses:
    - distance in million kilometres
    - mass in Earth masses
    - time in days
    - velocity in million kilometres per day
    """

    return [
        # Sun
        Body(
            "Sun",
            332946.05,
            25,
            0,
            0,
            -0.00120529,
            -0.00004326,
            (255, 220, 70),
        ),

        # Mercury
        Body(
            "Mercury",
            0.0553,
            5,
            43.6778,
            15.8974,
            -1.4455,
            4.8405,
            (170, 170, 170),
        ),

        # Venus
        Body(
            "Venus",
            0.815,
            7,
            27.9561,
            104.3334,
            -2.9228,
            0.8037,
            (230, 160, 80),
        ),

        # Earth
        Body(
            "Earth",
            1.0,
            8,
            -116.0514,
            97.3787,
            -1.6544,
            -1.9286,
            (70, 130, 240),
        ),

        # Mars
        Body(
            "Mars",
            0.107,
            6,
            -212.9156,
            -122.9269,
            1.0469,
            -1.6178,
            (210, 80, 60),
        ),

        # Jupiter
        Body(
            "Jupiter",
            317.828,
            14,
            -136.0132,
            -771.3689,
            1.1123,
            -0.1409,
            (220, 155, 95),
        ),

        # Saturn
        Body(
            "Saturn",
            95.159,
            12,
            970.5966,
            -970.5966,
            0.5891,
            0.6361,
            (200, 190, 120),
        ),

        # Uranus
        Body(
            "Uranus",
            14.536,
            10,
            2382.0946,
            1375.3030,
            -0.2942,
            0.5369,
            (100, 210, 210),
        ),

        # Neptune
        Body(
            "Neptune",
            17.147,
            10,
            -4541.1308,
            0,
            0,
            -0.4649,
            (80, 110, 220),
        ),
    ]