from attrs import frozen
import arcade

import protocols as proto
from vector import Vector2

MAX_DISTANCE_TO_PLAYER = 50
FROM_CENTER_PLAYER_DELTA = Vector2(0, -30)
POSITION_PREDICTION_TIME_DELTA = .01


@frozen
class Camera:
    _camera: arcade.Camera2D
    _player: proto.Player

    @property
    def camera(self) -> arcade.Camera2D:
        return self._camera

    def update(self, dt: float) -> None:
        camera_position = Vector2(*self._camera.position)
        player_rigid_body = self._player.rigid_body
        predicted_position = player_rigid_body.position + player_rigid_body.velocity * POSITION_PREDICTION_TIME_DELTA
        delta = predicted_position - FROM_CENTER_PLAYER_DELTA - camera_position
        speed = (delta.length / MAX_DISTANCE_TO_PLAYER)**2 * delta.length
        delta_position = delta.normalize * speed * dt
        self._camera.position = (camera_position + delta_position).tuple