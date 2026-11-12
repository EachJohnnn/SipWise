from typing import Literal

from pydantic import BaseModel


class Health(BaseModel):
    status: Literal["ok"] = "ok"
    database: Literal["ok"] = "ok"
    catalog: Literal["fixture"] = "fixture"


class CocktailSummary(BaseModel):
    id: str
    name: str
    image_url: str | None
    alcohol_type: Literal["alcoholic", "non_alcoholic", "optional", "unknown"]


class Ingredient(BaseModel):
    name: str
    measure: str | None


class Story(BaseModel):
    summary: str
    source_title: str
    source_url: str


class CocktailDetail(CocktailSummary):
    category: str | None
    glass: str | None
    ingredients: list[Ingredient]
    instructions: str | None
    recipe_source_url: str
    story: Story | None
