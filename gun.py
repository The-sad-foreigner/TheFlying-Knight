from time import time

from attrs import define, field

import protocols as proto
from vector import Vector2


@define
class Gun(proto.Gun):
    _shoot_frequency: float
    _shoot_delta: Vector2
    _bullet_speed: float
    _bullets: proto.Bullets

    _last_shot_time: float = field(init=False, factory=time)

    @property
    def can_shoot(self) -> bool:
        return time() - self._last_shot_time >= 1 / self._shoot_frequency

    def try_shoot(self, shooter_position: Vector2, bullet_direction: Vector2) -> bool:
        if not self.can_shoot:
            return False

        position = shooter_position + self._shoot_delta
        velocity = bullet_direction * self._bullet_speed
        self._bullets.spawn(position, velocity)
        self._last_shot_time = time()
        return True
