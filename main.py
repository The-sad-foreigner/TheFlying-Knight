import arcade

from bullets import Bullets
from player import (Player, SHAPE, MAX_SPEED, SHOOT_DELTA, SHOOT_FREQUENCY,
                    GRAVITY_ACCELERATION)
from draw import Draw
from vector import Vector2Int, Vector2
from game_engine import GameEngine
from rigid_body import RigidBody
from gun import Gun
from platform_ import Platform, MovingPlatform
from platforms import Platforms

TITLE = "Test"
SCREEN_SHAPE = Vector2Int(1080, 720)    # 1080, 720


def main() -> None:
    platforms = Platforms([
        Platform(RigidBody(Vector2(-10, -500), Vector2.zero(), Vector2.zero(), 0, Vector2(1080 + 20, 500))),
        Platform(RigidBody(Vector2(50, 50), Vector2.zero(), Vector2.zero(), 0, Vector2(200, 50))),
        MovingPlatform(RigidBody(Vector2(300, 50), Vector2.zero(), Vector2.zero(), 0, Vector2(200, 50)),
                       Vector2(300, 50), Vector2(500, 500), 12),
        Platform(RigidBody(Vector2(750, 500), Vector2.zero(), Vector2.zero(), 0, Vector2(200, 50))),
        Platform(RigidBody(Vector2(-10, 0), Vector2.zero(), Vector2.zero(), 0, Vector2(30, 600))),
        Platform(RigidBody(Vector2(1060, 0), Vector2.zero(), Vector2.zero(), 0, Vector2(30, 600))),
        Platform(RigidBody(Vector2(-1000, -1030), Vector2.zero(), Vector2.zero(), 0, Vector2(3080, 30))),
    ])
    bullets = Bullets()
    player = Player(RigidBody(SCREEN_SHAPE.with_x(100).as_vector2 * .5, Vector2.zero(), MAX_SPEED,  # SCREEN_SHAPE.with_x(100).as_vector2 * .5
                              GRAVITY_ACCELERATION, SHAPE),
                    Gun(SHOOT_FREQUENCY, SHOOT_DELTA, 1_000, bullets),
                    platforms)

    engine = GameEngine(TITLE, Vector2Int(1080, 720), Draw(), bullets, platforms, player)
    engine.mouse_clicked.subscribe(lambda position: _on_mouse_click(position, player))  # mouse_clicked
    engine.keyboard_state_changed.subscribe(lambda keys: _on_keyboard_state_changed(player, keys))

    engine.run()


def _on_mouse_click(position: Vector2, player: Player) -> None:
    direction = (position - player.rigid_body.position).normalize
    player.gun.try_shoot(player.rigid_body.position, direction)


def _on_keyboard_state_changed(player: Player, keys: set[int]) -> None:
    d_is_pressed = arcade.key.D in keys
    a_is_pressed = arcade.key.A in keys
    w_is_pressed = arcade.key.W in keys
    space_is_pressed = arcade.key.SPACE in keys
    lshift_is_pressed = arcade.key.LSHIFT in keys
    x = d_is_pressed - a_is_pressed
    if lshift_is_pressed:
        y = -(lshift_is_pressed * 100)
    else:
        y = -lshift_is_pressed

    direction = Vector2(x, y)
    direction = direction.normalize if direction.length > 0 else direction
    player.set_direction(direction)

    if w_is_pressed or space_is_pressed:
        player.try_jump()


if __name__ == "__main__":
    main()