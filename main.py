"""Run the interactive Solar-System simulation."""

import random

import pygame

from body import Body, create_solar_system
from camera import Camera
from energy import calculate_total_energy
from integrators import euler_step, velocity_verlet_step
from renderer import Renderer


# Size of the Pygame window.
WIDTH = 1280
HEIGHT = 720

# Time-scale settings.
REFERENCE_TIME_SCALE = 1.0
FAST_TIME_SCALE = 80.0

# Asteroid properties.
#
# Mass is measured in Earth masses, just like the planets.
# The range gives every asteroid a slightly different mass.
MIN_ASTEROID_MASS = 1e-6
MAX_ASTEROID_MASS = 1e-4

# Radius is mainly a visual size in this simulation.
MIN_ASTEROID_RADIUS = 1
MAX_ASTEROID_RADIUS = 5


def spawn_asteroid(
    bodies: list[Body],
    world_x: float,
    world_y: float,
) -> Body:
    """
    Create an asteroid at the clicked world position.

    The asteroid gets random physical and visual properties.
    Its velocity is also chosen directly rather than being
    calculated for a circular orbit.
    """

    # Give the asteroid a random mass within our chosen range.
    mass = random.uniform(
        MIN_ASTEROID_MASS,
        MAX_ASTEROID_MASS,
    )

    # Give the asteroid a random radius.
    radius = random.uniform(
        MIN_ASTEROID_RADIUS,
        MAX_ASTEROID_RADIUS,
    )

    # Give the asteroid an arbitrary starting velocity.
    #
    # The simulation will then let gravity change its motion.
    vx = random.uniform(-4.0, 4.0)
    vy = random.uniform(-4.0, 4.0)

    # Give the asteroid a random colour.
    color = (
        random.randrange(0, 256),
        random.randrange(0, 256),
        random.randrange(0, 256),
    )

    asteroid = Body(
        name=f"Asteroid {len(bodies) - 8}",
        mass=mass,
        radius=radius,
        x=world_x,
        y=world_y,
        vx=vx,
        vy=vy,
        color=color,
    )

    bodies.append(asteroid)

    return asteroid


def run() -> None:
    """Start and run the simulation."""

    # Start Pygame.
    pygame.init()

    # Create the game window.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "Academic Solar-System Orbit Simulator"
    )

    # Clock controls the frame rate and gives us the time
    # that passed between frames.
    clock = pygame.time.Clock()

    # Font used by the HUD and notifications.
    font = pygame.font.SysFont(None, 24)

    # Create the camera and renderer.
    camera = Camera(WIDTH, HEIGHT)
    renderer = Renderer(screen, camera)

    # Create the starting Solar System.
    bodies = create_solar_system()

    # Store the two integration methods.
    #
    # The first one is the default.
    integrators = [
        velocity_verlet_step,
        euler_step,
    ]

    integrator_names = [
        "Velocity Verlet",
        "Euler",
    ]

    integrator_index = 0

    # Simulation state.
    paused = False
    time_scale = REFERENCE_TIME_SCALE

    # Temporary notification shown at the top of the screen.
    notification = "Solar System initialized"
    notification_time = 2.0

    running = True

    while running:

        # Get the real time that passed since the previous frame.
        #
        # tick(60) also limits the program to roughly 60 FPS.
        real_dt = clock.tick(60) / 1000.0

        # Count down the notification timer.
        notification_time = max(
            0.0,
            notification_time - real_dt,
        )

        # Handle keyboard and mouse input.
        for event in pygame.event.get():

            # Close the program.
            if event.type == pygame.QUIT:
                running = False

            # Left-click creates an asteroid.
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                # Mouse coordinates are screen coordinates.
                # Convert them into world coordinates before
                # creating the asteroid.
                world_x, world_y = camera.screen_to_world(
                    *event.pos
                )

                spawn_asteroid(
                    bodies,
                    world_x,
                    world_y,
                )

                notification = "Asteroid added"
                notification_time = 2.0

            # Handle keyboard presses.
            elif event.type == pygame.KEYDOWN:

                # Space pauses or resumes the simulation.
                if event.key == pygame.K_SPACE:
                    paused = not paused

                    if paused:
                        notification = "Paused"
                    else:
                        notification = "Running"

                    notification_time = 2.0

                # R resets everything to the starting state.
                elif event.key == pygame.K_r:
                    bodies = create_solar_system()
                    camera.reset()
                    integrator_index = 0
                    time_scale = REFERENCE_TIME_SCALE
                    paused = False

                    notification = "Simulation reset"
                    notification_time = 2.0

                # E switches between the two integration methods.
                elif event.key == pygame.K_e:
                    integrator_index = 1 - integrator_index

                    notification = (
                        f"Integrator: "
                        f"{integrator_names[integrator_index]}"
                    )
                    notification_time = 2.0

                # M switches to the faster time scale.
                elif event.key == pygame.K_m:
                    time_scale = FAST_TIME_SCALE

                # N returns to normal time scale.
                elif event.key == pygame.K_n:
                    time_scale = REFERENCE_TIME_SCALE

                # Increase the time scale.
                elif event.key == pygame.K_UP:
                    time_scale += 10

                # Decrease the time scale.
                elif event.key == pygame.K_DOWN:
                    time_scale = max(
                        1,
                        time_scale - 10,
                    )

        # Read the currently held movement keys.
        keys = pygame.key.get_pressed()

        direction_x = (
            float(keys[pygame.K_d])
            - float(keys[pygame.K_a])
        )

        direction_y = (
            float(keys[pygame.K_s])
            - float(keys[pygame.K_w])
        )

        # I zooms in.
        # O zooms out.
        if keys[pygame.K_i]:
            zoom_factor = 1.01
        elif keys[pygame.K_o]:
            zoom_factor = 1 / 1.01
        else:
            zoom_factor = 1.0

        # Move the camera.
        camera.update(
            direction_x,
            direction_y,
            real_dt,
            zoom_factor,
        )

        # Only update the physics while the simulation is running.
        if not paused:
            dt = real_dt * time_scale

            integrators[integrator_index](
                bodies,
                dt,
            )

        # Calculate the total mechanical energy.
        total_energy = calculate_total_energy(bodies)

        # Draw everything.
        renderer.draw_background()
        renderer.draw(bodies)

        renderer.draw_hud(
            [
                f"FPS: {clock.get_fps():.1f}",
                f"Bodies: {len(bodies)}",
                f"Zoom: {camera.zoom:.2f}x",
                f"Time scale: {time_scale:.0f}x",
                f"State: {'Paused' if paused else 'Running'}",
                f"Integrator: {integrator_names[integrator_index]}",
                f"Total energy: {total_energy:.4f}",
                "E: switch integrator | Click: spawn asteroid",
            ],
            font,
        )

        # Draw the notification if it is still active.
        if notification_time > 0:
            renderer.draw_notification(
                notification,
                font,
            )

        # Show the completed frame.
        pygame.display.flip()

    # Shut down Pygame when the simulation ends.
    pygame.quit()


if __name__ == "__main__":
    run()