from typing import Callable

from attrs import define

import protocols as proto


@define
class Platforms(proto.Platforms):
    _platforms: list[proto.Platform]

    def get_touched(self, other: proto.RigidBody) -> proto.Platform | None:
        for platform in self._platforms:
            if platform.rigid_body.is_collided_with(other):
                return platform
        return None

    def update(self, dt: float) -> None:
        for platform in self._platforms:
            platform.update(dt)

    def apply(self, function: Callable[[proto.Platform], None]) -> None:
        for platform in self._platforms:
            function(platform)