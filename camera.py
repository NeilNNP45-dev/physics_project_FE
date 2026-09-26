"""Camera movement and conversion between world and screen coordinates."""


class Camera:
    """
    Controls what part of the simulation we can see.

    The simulation has its own coordinate system called the "world".

    Pygame has a different coordinate system called the "screen".

    The camera connects these two coordinate systems and also
    controls how much we are zoomed in or out.
    """

    def __init__(
        self,
        width: int,
        height: int,
        x: float = 0.0,
        y: float = 0.0,
        zoom: float = 0.25,
    ) -> None:
        # Size of the Pygame window.
        self.width = width
        self.height = height

        # Remember the starting camera position and zoom.
        # We use these values when the simulation is reset.
        self.initial_x = x
        self.initial_y = y
        self.initial_zoom = zoom

        # Current position of the camera in world coordinates.
        self.x = x
        self.y = y

        # How much we are zoomed in.
        #
        # A larger number means we are more zoomed in.
        # A smaller number means we are more zoomed out.
        self.zoom = zoom

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """
        Convert a position from the simulation's world to the screen.

        The simulation might have a planet at a world position such as:
            (100, 50)

        But Pygame needs a pixel position on the screen.

        The camera position is subtracted first so that moving the
        camera changes where the object appears on the screen.

        We then multiply by zoom to make the object appear closer
        or farther away.

        Finally, we add half the screen width and height because
        we want the camera's position to appear at the centre
        of the screen.
        """

        screen_x = (x - self.x) * self.zoom + self.width / 2
        screen_y = (y - self.y) * self.zoom + self.height / 2

        return screen_x, screen_y

    def screen_to_world(
        self,
        screen_x: float,
        screen_y: float,
    ) -> tuple[float, float]:
        """
        Convert a screen position back into a world position.

        This is basically the reverse of world_to_screen().

        We need this when the user clicks the screen.

        For example:

            mouse click
                ↓
            screen position
                ↓
            world position
                ↓
            create asteroid there

        This lets the user interact with the simulation using
        normal mouse coordinates.
        """

        world_x = (
            (screen_x - self.width / 2) / self.zoom
            + self.x
        )

        world_y = (
            (screen_y - self.height / 2) / self.zoom
            + self.y
        )

        return world_x, world_y

    def update(
        self,
        direction_x: float,
        direction_y: float,
        dt: float,
        zoom_factor: float = 1.0,
        movement_speed: float = 500.0,
    ) -> None:
        """
        Move the camera and update its zoom.

        direction_x and direction_y tell us which direction
        the camera should move.

        dt means "delta time".
        It tells us how much real time passed since the last frame.

        Using dt makes camera movement consistent even if the
        computer's frame rate changes.
        """

        # Move the camera horizontally.
        #
        # We divide by zoom so that camera movement feels
        # similar at different zoom levels.
        self.x += (
            direction_x
            * movement_speed
            * dt
            / self.zoom
        )

        # Move the camera vertically.
        self.y += (
            direction_y
            * movement_speed
            * dt
            / self.zoom
        )

        # Change the zoom level.
        #
        # The min and max values stop the camera from becoming
        # ridiculously zoomed in or zoomed out.
        self.zoom = max(
            0.01,
            min(10.0, self.zoom * zoom_factor),
        )

    def reset(self) -> None:
        """Return the camera to its original position and zoom."""

        self.x = self.initial_x
        self.y = self.initial_y
        self.zoom = self.initial_zoom