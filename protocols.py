from abc import ABC, abstractmethod
from typing import Callable

from vector import Vector2


class Bullet(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector2:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Bullets(ABC):
    @abstractmethod
    def spawn(self, position: Vector2, velocity: Vector2) -> None:
        ...

    @abstractmethod
    def kill(self, bullet: Bullet) -> None:
        ...

    @abstractmethod
    def apply(self, function: Callable[[Bullet], None]) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Gun:
    @property
    @abstractmethod
    def can_shoot(self) -> bool:
        ...

    @abstractmethod
    def try_shoot(self, shooter_position: Vector2, bullet_direction: Vector2) -> bool:
        ...


class RigidBody(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector2:
        ...

    @property
    @abstractmethod
    def velocity(self) -> Vector2:
        ...

    @property
    @abstractmethod
    def shape(self) -> Vector2:
        ...

    @abstractmethod
    def is_contain(self, point: Vector2) -> bool:
        ...

    @abstractmethod
    def is_collided_with(self, other: "RigidBody") -> bool:
        ...

    @abstractmethod
    def set_position(self, position: Vector2) -> None:
        ...

    @abstractmethod
    def set_velocity(self, velocity: Vector2) -> None:
        ...

    @abstractmethod
    def update(self, drag_ratio: float, acceleration: Vector2, dt: float) -> None:
        ...


class Player(ABC):
    @property
    @abstractmethod
    def rigid_body(self) -> RigidBody:
        ...

    @property
    @abstractmethod
    def gun(self) -> Gun:
        ...

    @abstractmethod
    def set_direction(self, direction: Vector2) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Platform(ABC):
    @property
    @abstractmethod
    def rigid_body(self) -> RigidBody:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

class Platforms(ABC):
    @abstractmethod
    def get_touched(self, other: RigidBody) -> Platform | None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def apply(self, function: Callable[[Platform], None]) -> None:
        ...