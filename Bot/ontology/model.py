from dataclasses import dataclass
from datetime import timedelta

@dataclass
class Country:
    iri: str
    name: str
    recipes: int

@dataclass
class Step:
    description: str
    next: str | None
    prev: str | None

@dataclass
class Recipe:
    iri: str
    title: str
    preparation_time: timedelta
    initial_step: str
    difficulty: str

@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: str

@dataclass
class Dish:
    iri: str
    name: str
    recipes: list[Recipe]
