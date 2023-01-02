from dataclasses import dataclass

@dataclass
class Country:
    name: str

@dataclass
class Step:
    description: str
    next: int | None
    prev: int | None

@dataclass
class Recipe:
    name: str
    initialStep: int
