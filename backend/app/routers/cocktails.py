from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..database import connect
from ..schemas import CocktailDetail, CocktailSummary

router = APIRouter(prefix="/cocktails", tags=["cocktails"])


@router.get("/search", response_model=list[CocktailSummary])
def search(name: Annotated[str, Query(min_length=1, max_length=100)]) -> list[CocktailDetail]:
    term = name.strip().casefold()
    if not term:
        raise HTTPException(422, "Enter a cocktail name")

    with connect() as connection:
        rows = connection.execute("SELECT payload_json FROM cocktails ORDER BY id").fetchall()

    recipes = [CocktailDetail.model_validate_json(payload) for (payload,) in rows]
    return [recipe for recipe in recipes if term in recipe.name.casefold()]


@router.get("/{cocktail_id}", response_model=CocktailDetail)
def detail(cocktail_id: str) -> CocktailDetail:
    with connect() as connection:
        row = connection.execute(
            "SELECT payload_json FROM cocktails WHERE id = ?", (cocktail_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(404, "Cocktail not found")
    return CocktailDetail.model_validate_json(row[0])
