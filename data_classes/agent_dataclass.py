from dataclasses import dataclass

@dataclass
class RLAgent:
    ammo: int
    lat: float = 0.0
    long: float = 0.0
    alt: float = 0.0
    vel: float = 0.0
    heading: float = 0.0


@dataclass
class BTAgent:
    ammo: int
    lat: float = 0.0
    long: float = 0.0
    alt: float = 0.0
    vel: float = 0.0
    heading: float = 0.0
