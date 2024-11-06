from dataclasses import dataclass


@dataclass
class Point:
    """
    A point in the scene.
    """
    lng: float
    lat: float


class SceneObject:
    """
    Base class for all scene objects.
    """
    def __init__(self, name, position: Point = None, address=None, description=None, tour_time= 1, open_time="全天开放",
                 scene_type: str = None):
        self.name = name
        self.position = position
        self.address = address
        self.description = description
        self.tour_time = tour_time
        self.open_time = open_time
        self.scene_type = scene_type
        self.extend_info = {}

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"




