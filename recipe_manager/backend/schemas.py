from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=100)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(default="", max_length=255)


class CategoryOut(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = ""
    ingredients: str
    instructions: str
    prep_time: int = Field(default=0, ge=0)
    cook_time: int = Field(default=0, ge=0)
    servings: int = Field(default=1, ge=1)
    category_id: int | None = None


class RecipeOut(RecipeCreate):
    id: int
    owner_id: int
    image: str | None
    created_at: datetime
    category: CategoryOut | None = None
    is_favorite: bool = False

    model_config = ConfigDict(from_attributes=True)
