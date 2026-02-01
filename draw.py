from dataclasses import dataclass

import arcade

import protocols as proto

BULLET_RADIUS = 10
BULLET_COLOR = arcade.color.BLACK

PLAYER_COLOR = arcade.color.GRAPE
PLATFORM_COLOR = arcade.color.GREEN


@dataclass
class Draw:
    def bullet(self, bullet: proto.Bullet) -> None:
        arcade.draw_circle_filled(*bullet.position.tuple, BULLET_RADIUS, BULLET_COLOR)

    def bullets(self, bullets: proto.Bullets) -> None:
        bullets.apply(self.bullet)

    def platforms(self, platforms: proto.Platforms) -> None:
        platforms.apply(self.platform)

    def player(self, player: proto.Player) -> None:
        position = player.rigid_body.position
        rect = arcade.rect.LBWH(*position.tuple, *player.rigid_body.shape.tuple)
        arcade.draw_rect_filled(rect, PLAYER_COLOR)

    def platform(self, platform: proto.Platform) -> None:
        position = platform.rigid_body.position
        rect = arcade.rect.LBWH(*position.tuple, *platform.rigid_body.shape.tuple)
        arcade.draw_rect_filled(rect, PLATFORM_COLOR)