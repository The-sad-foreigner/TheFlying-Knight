from dataclasses import dataclass, field
from typing import Callable

import protocols as proto
from vector import Vector2
from bullet import Bullet

PLAYER: list[Vector2]

@dataclass(frozen=True)
class Bullets(proto.Bullets):

    _bullets: list[proto.Bullet] = field(init=False, default_factory=list)
    _player: list[proto.Bullet] = field(init=False, default_factory=list)


    def spawn(self, position: Vector2, velocity: Vector2) -> None:
        self._player.append(Bullet(position, velocity))
        bullet = Bullet(position, velocity)
        self._bullets.append(bullet)

    def kill(self, bullet: proto.Bullet) -> None:
        assert bullet in self._bullets

        self._bullets.remove(bullet)
        del self._player[0]

    def apply(self, function: Callable[[proto.Bullet], None]) -> None:
        for bullet in self._bullets:
            function(bullet)

    def update(self, dt: float) -> None:
        for bullet in self._bullets:
            bullet.update(dt)
            if self._is_bullet_out_of_screen(bullet):
                self.kill(bullet)

    def _is_bullet_out_of_screen(self, bullet: proto.Bullet) -> bool:
        position = bullet.position
        player = self._player
        return not (player[-1].position.x - 500.0 <= position.x < player[-1].position.x + 500.0 and
                    player[-1].position.y - 500.0 <= position.y < player[-1].position.y + 500.0)