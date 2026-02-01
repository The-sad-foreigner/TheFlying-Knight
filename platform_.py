from time import time
from math import sin, tau

from attrs import frozen, field

import protocols as proto
from vector import Vector2

@frozen
class Platform(proto.Platform):
    _rigid_body: proto.RigidBody

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    def update(self, dt: float) -> None:
        ...


@frozen
class MovingPlatform(proto.Platform):
    _rigid_body: proto.RigidBody
    _start_position: Vector2
    _stop_position: Vector2
    _period: float

    _start_time: float = field(init=False, factory=time)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    @property
    def _center(self) -> Vector2:
        return self._start_position + self._delta * .5

    @property
    def _delta(self) -> Vector2:
        return self._stop_position - self._start_position

    def update(self, dt: float) -> None:
        delta_time = time() - self._start_time
        last_position = self.rigid_body.position
        position = self._center + self._delta * sin(tau * delta_time / self._period) * .5
        self.rigid_body.set_position(position)
        self.rigid_body.set_velocity((position - last_position) * (1 / delta_time))