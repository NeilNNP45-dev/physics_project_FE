"""Draw the bodies, trails, stars, and information on the screen."""

import random

import pygame

from body import Body
from camera import Camera


class Renderer:
    """
    Handles everything that is drawn on the screen.

    This class does not calculate physics.
    It only takes the information from the simulation
    and turns it into something we can see.
    """

    def __init__(self, screen: pygame.Surface, camera: Camera) -> None:
        # The Pygame window where everything will be drawn.
        self.screen = screen

        # The camera tells us how to convert positions from
        # the simulation's world into screen positions.
        self.camera = camera

        # Store the background stars.
        #
        # Each star is stored as:
        #
        #     (x position, y position, size, brightness, shape)
        #
        # The positions are screen coordinates because the
        # background does not move with the camera.
        self.stars = []

        # Create 90 stars.
        for _ in range(90):
            x = random.randrange(camera.width)
            y = random.randrange(camera.height)

            # Most stars are very small.
            # A few stars are slightly larger so the background
            # has some visual variety.
            size = random.choice((1, 1, 1, 1, 2, 2, 3))

            # Give each star a slightly different brightness.
            #
            # This prevents every star from looking identical.
            brightness = random.randrange(100, 231)

            # Pick a simple geometric shape for the star.
            #
            # Diamonds are the most common.
            # Crosses and four-point stars are less common.
            shape = random.choices(
                ["diamond", "cross", "four_point"],
                weights=[70, 20, 10],
                k=1,
            )[0]

            self.stars.append(
                (x, y, size, brightness, shape)
            )

    def draw_background(self) -> None:
        """Draw the black space background and its stars."""

        # Fill the entire window with pure black.
        self.screen.fill((0, 0, 0))

        # Draw every star that we created when the renderer started.
        for x, y, size, brightness, shape in self.stars:

            # Use the same brightness for all three colour channels.
            #
            # This gives us neutral white/gray stars instead of
            # making the background strongly blue or purple.
            color = (
                brightness,
                brightness,
                brightness,
            )

            if shape == "diamond":
                # A diamond has sharp edges and is useful for
                # most of the small background stars.
                points = [
                    (x, y - size),
                    (x + size, y),
                    (x, y + size),
                    (x - size, y),
                ]

                pygame.draw.polygon(
                    self.screen,
                    color,
                    points,
                )

            elif shape == "cross":
                # Draw a small sharp cross.
                #
                # This gives the background some variation without
                # making every star look decorative.
                pygame.draw.line(
                    self.screen,
                    color,
                    (x - size, y),
                    (x + size, y),
                    1,
                )

                pygame.draw.line(
                    self.screen,
                    color,
                    (x, y - size),
                    (x, y + size),
                    1,
                )

            else:
                # Draw a four-point star.
                #
                # This is used less often so that brighter stars
                # stand out from the smaller background stars.
                points = [
                    (x, y - size),
                    (x + 1, y - 1),
                    (x + size, y),
                    (x + 1, y + 1),
                    (x, y + size),
                    (x - 1, y + 1),
                    (x - size, y),
                    (x - 1, y - 1),
                ]

                pygame.draw.polygon(
                    self.screen,
                    color,
                    points,
                )

    def draw_body(self, body: Body) -> None:
        """Draw one body's trail and the body itself."""

        # Draw the trail only when there are at least two points.
        #
        # A single point cannot make a visible line.
        if len(body.trail) > 1:

            # The trail positions are stored in world coordinates.
            # Convert every point into screen coordinates before
            # giving them to Pygame.
            points = [
                self.camera.world_to_screen(x, y)
                for x, y in body.trail
            ]

            # Pygame needs integer pixel positions for drawing.
            screen_points = [
                (int(x), int(y))
                for x, y in points
            ]

            # Draw a line connecting all of the trail points.
            pygame.draw.lines(
                self.screen,
                body.color,
                False,
                screen_points,
                1,
            )

        # Convert the body's current world position into a
        # position on the screen.
        x, y = self.camera.world_to_screen(
            body.x,
            body.y,
        )

        # Convert the body's visual radius into pixels.
        #
        # Zoom affects how large the body appears on screen.
        #
        # max(1, ...) makes sure the body is always at least
        # one pixel wide, even when we are zoomed far out.
        radius = max(
            1,
            int(body.radius * self.camera.zoom),
        )

        # Draw the body as a filled circle.
        pygame.draw.circle(
            self.screen,
            body.color,
            (int(x), int(y)),
            radius,
        )

    def draw(self, bodies: list[Body]) -> None:
        """Draw every body in the simulation."""

        # Go through the list of bodies one at a time.
        for body in bodies:
            self.draw_body(body)

    def draw_hud(
        self,
        lines: list[str],
        font: pygame.font.Font,
    ) -> None:
        """
        Draw information such as FPS, energy, and controls.

        The HUD means "Heads-Up Display".
        It is the text information shown on top of the simulation.
        """

        # Draw each line below the previous one.
        for index, line in enumerate(lines):

            # Turn the text into a Pygame surface.
            surface = font.render(
                line,
                True,
                (240, 240, 240),
            )

            # Draw the text near the top-left corner.
            #
            # Each line is moved 25 pixels lower than the previous one.
            self.screen.blit(
                surface,
                (10, 10 + index * 25),
            )

    def draw_notification(
        self,
        message: str,
        font: pygame.font.Font,
    ) -> None:
        """Draw a temporary message near the top of the screen."""

        # Convert the message into something Pygame can draw.
        surface = font.render(
            message,
            True,
            (255, 255, 255),
        )

        # Put the message in the horizontal centre of the screen.
        #
        # surface.get_width() tells us how wide the text is,
        # so we can calculate the correct starting position.
        x = (
            self.camera.width - surface.get_width()
        ) // 2

        self.screen.blit(
            surface,
            (x, 25),
        )