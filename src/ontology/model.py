from dataclasses import dataclass
from datetime import timedelta

@dataclass
class Country:
    iri: str
    name: str
    recipes: int

@dataclass
class Recipe:
    iri: str
    title: str
    preparation_time: timedelta
    initial_step: any
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
