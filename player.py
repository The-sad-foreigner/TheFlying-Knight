from attrs import define, field

import protocols as proto
from vector import Vector2

SHAPE = Vector2(40, 60)

SHOOT_FREQUENCY = 30.7
SHOOT_DELTA = SHAPE * .5

MAX_SPEED = Vector2(300, float('inf'))
ACCELERATION = 5_000

GRAVITY_ACCELERATION = 5_000

AIR_DRAG_RATIO = 2
GROUNDED_DRAG_RATIO = 5
GROUND_DRAUGHT = 3

JUMP_SPEED = 1_500


@define
class Player(proto.Player):
    _rigid_body: proto.RigidBody
    _gun: proto.Gun
    _platforms: proto.Platforms

    _direction: Vector2 = field(init=False, default=Vector2.zero())

    @property
    def gun(self) -> proto.Gun:
        return self._gun

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    def get_ground(self) -> proto.Platform | None:
        return self._platforms.get_touched(self.rigid_body)

    def set_direction(self, direction: Vector2) -> None:
        assert direction.length <= 1.00001
        self._direction = direction

    def try_jump(self) -> bool:
        if not self.get_ground():
            return False

        velocity = self.rigid_body.velocity.with_y(JUMP_SPEED)
        self.rigid_body.set_velocity(velocity)
        return True

    def update(self, dt: float) -> None:
        acceleration = self._direction * ACCELERATION
        drag_ratio = GROUNDED_DRAG_RATIO if self.get_ground() else AIR_DRAG_RATIO
        self._rigid_body.update(drag_ratio, acceleration, dt)

        ground = self.get_ground()
        if not ground:
            return

        y = self.rigid_body.position.y
        if y < ground.rigid_body.position.y:
            return

        self.rigid_body.set_velocity(self.rigid_body.velocity.with_y(ground.rigid_body.velocity.y))

        ground_level = ground.rigid_body.position.y + ground.rigid_body.shape.y
        self.rigid_body.set_position(self.rigid_body.position.with_y(ground_level - GROUND_DRAUGHT))