import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from ..auth import get_current_user
from ..database import get_db
from ..models import Category, Recipe, User
from ..schemas import RecipeCreate, RecipeOut

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/recipes", tags=["Recipes"])


def to_output(recipe: Recipe, user: User):
    data = RecipeOut.model_validate(recipe).model_dump()
    data["is_favorite"] = any(u.id == user.id for u in recipe.favorited_by)
    return data


@router.get("", response_model=list[RecipeOut])
def list_recipes(
    search: str = "",
    category_id: int | None = None,
    favorites_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.favorited_by),
    ).filter(Recipe.owner_id == current_user.id)

    if search.strip():
        query = query.filter(Recipe.title.ilike(f"%{search.strip()}%"))

    if category_id:
        query = query.filter(Recipe.category_id == category_id)

    recipes = query.order_by(Recipe.created_at.desc()).all()

    if favorites_only:
        recipes = [r for r in recipes if any(u.id == current_user.id for u in r.favorited_by)]

    return [to_output(r, current_user) for r in recipes]


@router.get("/{recipe_id}", response_model=RecipeOut)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.favorited_by),
    ).filter(
        Recipe.id == recipe_id,
        Recipe.owner_id == current_user.id,
    ).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return to_output(recipe, current_user)


@router.post("", response_model=RecipeOut, status_code=201)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.category_id:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    recipe = Recipe(
        **data.model_dump(),
        owner_id=current_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return to_output(recipe, current_user)


@router.put("/{recipe_id}", response_model=RecipeOut)
def update_recipe(
    recipe_id: int,
    data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.favorited_by),
    ).filter(
        Recipe.id == recipe_id,
        Recipe.owner_id == current_user.id,
    ).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if data.category_id:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    for key, value in data.model_dump().items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)
    return to_output(recipe, current_user)


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.owner_id == current_user.id,
    ).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"message": "Recipe deleted"}


@router.post("/{recipe_id}/favorite", response_model=RecipeOut)
def toggle_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.favorited_by),
    ).filter(
        Recipe.id == recipe_id,
        Recipe.owner_id == current_user.id,
    ).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if current_user in recipe.favorited_by:
        recipe.favorited_by.remove(current_user)
    else:
        recipe.favorited_by.append(current_user)

    db.commit()
    db.refresh(recipe)
    return to_output(recipe, current_user)


@router.post("/{recipe_id}/image", response_model=RecipeOut)
async def upload_image(
    recipe_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.favorited_by),
    ).filter(
        Recipe.id == recipe_id,
        Recipe.owner_id == current_user.id,
    ).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    allowed = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Use JPG, PNG or WEBP")

    ext = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }[file.content_type]

    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as output:
        output.write(await file.read())

    recipe.image = filename
    db.commit()
    db.refresh(recipe)
    return to_output(recipe, current_user)
