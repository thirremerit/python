# Recipe Manager

A complete recipe-management web application using:

- **FastAPI** — backend REST API
- **SQLite + SQLAlchemy** — database
- **Streamlit** — frontend

## Features

- User registration and login
- Secure password hashing
- JWT authentication
- Create, edit and delete recipes
- Create, edit and delete categories
- Search recipes
- Filter by category
- Favorite/unfavorite recipes
- Recipe images
- Preparation/cooking time and servings
- Dashboard with recipe statistics
- Clean Streamlit UI

## 1. Install

Open a terminal in this folder:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

## 2. Start the backend

From the project folder:

```bash
uvicorn backend.main:app --reload
```

The API will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## 3. Start the frontend

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The frontend normally opens at:

http://localhost:8501

## Project structure

```text
recipe_manager/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       ├── categories.py
│       └── recipes.py
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   └── api.py
├── uploads/
├── data/
├── requirements.txt
└── README.md
```

## Notes

The SQLite database is created automatically at `data/recipes.db`.

Uploaded images are stored in `uploads/`.

For a school project, this is a strong starting point. In a production deployment you would move the secret key to an environment variable and use a production database such as PostgreSQL.
