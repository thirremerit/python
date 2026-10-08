from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table, Boolean
from sqlalchemy.orm import relationship
from .database import Base

recipe_favorites = Table(
    "recipe_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)

    recipes = relationship("Recipe", back_populates="owner", cascade="all, delete-orphan")
    favorites = relationship(
        "Recipe",
        secondary=recipe_favorites,
        back_populates="favorited_by",
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255), default="")

    recipes = relationship("Recipe", back_populates="category")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, default="")
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer, default=0)
    cook_time = Column(Integer, default=0)
    servings = Column(Integer, default=1)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    owner = relationship("User", back_populates="recipes")
    category = relationship("Category", back_populates="recipes")
    favorited_by = relationship(
        "User",
        secondary=recipe_favorites,
        back_populates="favorites",
    )
