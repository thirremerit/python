import requests
import streamlit as st

from api import API_URL, request

st.set_page_config(
    page_title="Recipe Manager",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def go(page):
    st.session_state.page = page
    st.rerun()


def error_box(e):
    st.error(f"Something went wrong: {e}")


def login_screen():
    st.title("🍳 Recipe Manager")
    st.caption("Organize your recipes in one simple place.")

    tab1, tab2 = st.tabs(["Login", "Create account"])

    with tab1:
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            try:
                result = requests.post(
                    f"{API_URL}/users/login",
                    json={
                        "username": username,
                        "email": "unused@example.com",
                        "password": password,
                    },
                    timeout=15,
                )
                if not result.ok:
                    raise Exception(result.json().get("detail", "Login failed"))
                st.session_state.token = result.json()["access_token"]
                st.rerun()
            except Exception as e:
                error_box(e)

    with tab2:
        with st.form("register"):
            username = st.text_input("Username", key="reg_user")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            password2 = st.text_input("Confirm password", type="password")
            submit = st.form_submit_button("Create account", use_container_width=True)

        if submit:
            if password != password2:
                st.error("Passwords do not match.")
            else:
                try:
                    result = requests.post(
                        f"{API_URL}/users/register",
                        json={
                            "username": username,
                            "email": email,
                            "password": password,
                        },
                        timeout=15,
                    )
                    if not result.ok:
                        raise Exception(result.json().get("detail", "Registration failed"))
                    st.success("Account created. You can now log in.")
                except Exception as e:
                    error_box(e)


def sidebar():
    with st.sidebar:
        st.title("🍳 Recipe Manager")
        st.caption("Your personal recipe collection")

        pages = {
            "📊 Dashboard": "Dashboard",
            "📖 My Recipes": "Recipes",
            "➕ Add Recipe": "Add Recipe",
            "🗂️ Categories": "Categories",
            "⭐ Favorites": "Favorites",
        }

        for label, page in pages.items():
            if st.button(label, use_container_width=True):
                go(page)

        st.divider()

        if st.button("🚪 Log out", use_container_width=True):
            st.session_state.token = None
            st.rerun()


def get_categories():
    return request("GET", "/categories", st.session_state.token)


def get_recipes(search="", category_id=None, favorites=False):
    params = {"search": search, "favorites_only": favorites}
    if category_id:
        params["category_id"] = category_id
    return request("GET", "/recipes", st.session_state.token, params=params)


def dashboard():
    st.title("📊 Dashboard")
    st.write("Welcome to your recipe collection.")

    try:
        recipes = get_recipes()
        categories = get_categories()
    except Exception as e:
        error_box(e)
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Recipes", len(recipes))
    c2.metric("Categories", len(categories))
    c3.metric("Favorites", sum(r["is_favorite"] for r in recipes))

    st.divider()
    st.subheader("Recent recipes")

    if not recipes:
        st.info("You haven't added any recipes yet. Use **Add Recipe** to get started.")
        return

    for recipe in recipes[:6]:
        recipe_card(recipe)


def recipe_card(recipe):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            if recipe.get("image"):
                st.image(
                    f"{API_URL}/uploads/{recipe['image']}",
                    use_container_width=True,
                )
            else:
                st.markdown("### 🍽️")

        with col2:
            fav = "⭐" if recipe["is_favorite"] else "☆"
            st.subheader(f"{fav} {recipe['title']}")

            category = recipe.get("category")
            st.caption(category["name"] if category else "Uncategorized")

            if recipe.get("description"):
                st.write(recipe["description"])

            st.write(
                f"⏱️ {recipe['prep_time'] + recipe['cook_time']} min  •  "
                f"👥 {recipe['servings']} servings"
            )

            if st.button("View / Edit", key=f"view_{recipe['id']}"):
                st.session_state.selected_recipe = recipe["id"]
                go("Recipe")


def recipe_page(recipe_id):
    try:
        recipe = request("GET", f"/recipes/{recipe_id}", st.session_state.token)
        categories = get_categories()
    except Exception as e:
        error_box(e)
        return

    st.title(f"🍽️ {recipe['title']}")

    if recipe.get("image"):
        st.image(f"{API_URL}/uploads/{recipe['image']}", width=500)

    st.caption(
        f"{recipe.get('category', {}).get('name', 'Uncategorized')} • "
        f"{recipe['prep_time']} min prep • {recipe['cook_time']} min cook • "
        f"{recipe['servings']} servings"
    )

    if recipe.get("description"):
        st.write(recipe["description"])

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("🧂 Ingredients")
        st.text(recipe["ingredients"])

    with right:
        st.subheader("👨‍🍳 Instructions")
        st.text(recipe["instructions"])

    st.divider()

    if st.button(
        "⭐ Remove from favorites" if recipe["is_favorite"] else "☆ Add to favorites"
    ):
        try:
            request(
                "POST",
                f"/recipes/{recipe_id}/favorite",
                st.session_state.token,
            )
            st.rerun()
        except Exception as e:
            error_box(e)

    with st.expander("Edit recipe"):
        edit_recipe_form(recipe, categories)

    with st.expander("Upload / replace image"):
        image = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"image_{recipe_id}",
        )
        if image and st.button("Upload image", key=f"upload_{recipe_id}"):
            try:
                request(
                    "POST",
                    f"/recipes/{recipe_id}/image",
                    st.session_state.token,
                    files={"file": (image.name, image.getvalue(), image.type)},
                )
                st.success("Image uploaded.")
                st.rerun()
            except Exception as e:
                error_box(e)

    if st.button("🗑️ Delete recipe", type="primary"):
        try:
            request("DELETE", f"/recipes/{recipe_id}", st.session_state.token)
            st.session_state.page = "Recipes"
            st.success("Recipe deleted.")
            st.rerun()
        except Exception as e:
            error_box(e)


def edit_recipe_form(recipe, categories):
    names = ["Uncategorized"] + [c["name"] for c in categories]
    current = recipe.get("category")
    current_name = current["name"] if current else "Uncategorized"

    with st.form(f"edit_{recipe['id']}"):
        title = st.text_input("Title", recipe["title"])
        description = st.text_area("Description", recipe.get("description", ""))
        ingredients = st.text_area("Ingredients", recipe["ingredients"], height=180)
        instructions = st.text_area("Instructions", recipe["instructions"], height=220)

        c1, c2, c3 = st.columns(3)
        prep = c1.number_input("Prep time (min)", 0, 1000, recipe["prep_time"])
        cook = c2.number_input("Cook time (min)", 0, 1000, recipe["cook_time"])
        servings = c3.number_input("Servings", 1, 100, recipe["servings"])

        category_name = st.selectbox(
            "Category",
            names,
            index=names.index(current_name) if current_name in names else 0,
        )

        save = st.form_submit_button("Save changes", use_container_width=True)

    if save:
        category_id = None
        if category_name != "Uncategorized":
            category_id = next(
                c["id"] for c in categories if c["name"] == category_name
            )

        try:
            request(
                "PUT",
                f"/recipes/{recipe['id']}",
                st.session_state.token,
                json={
                    "title": title,
                    "description": description,
                    "ingredients": ingredients,
                    "instructions": instructions,
                    "prep_time": prep,
                    "cook_time": cook,
                    "servings": servings,
                    "category_id": category_id,
                },
            )
            st.success("Recipe updated.")
            st.rerun()
        except Exception as e:
            error_box(e)


def recipes_page(favorites=False):
    st.title("⭐ Favorites" if favorites else "📖 My Recipes")

    try:
        categories = get_categories()
    except Exception as e:
        error_box(e)
        return

    search = st.text_input("🔍 Search recipes", placeholder="Search by recipe name...")

    category_options = ["All categories"] + [c["name"] for c in categories]
    selected = st.selectbox("Category", category_options)

    category_id = None
    if selected != "All categories":
        category_id = next(c["id"] for c in categories if c["name"] == selected)

    try:
        recipes = get_recipes(search, category_id, favorites)
    except Exception as e:
        error_box(e)
        return

    st.caption(f"{len(recipes)} recipe(s) found")

    if not recipes:
        st.info("No recipes match your search.")
        return

    for recipe in recipes:
        recipe_card(recipe)


def add_recipe():
    st.title("➕ Add Recipe")
    st.write("Create a new recipe for your collection.")

    try:
        categories = get_categories()
    except Exception as e:
        error_box(e)
        return

    names = ["Uncategorized"] + [c["name"] for c in categories]

    with st.form("add_recipe"):
        title = st.text_input("Recipe title")
        description = st.text_area("Short description")
        ingredients = st.text_area(
            "Ingredients",
            placeholder="1 cup flour\n2 eggs\n...",
            height=180,
        )
        instructions = st.text_area(
            "Instructions",
            placeholder="1. Mix...\n2. Cook...",
            height=220,
        )

        c1, c2, c3 = st.columns(3)
        prep = c1.number_input("Prep time (min)", 0, 1000, 10)
        cook = c2.number_input("Cook time (min)", 0, 1000, 20)
        servings = c3.number_input("Servings", 1, 100, 2)

        category_name = st.selectbox("Category", names)
        image = st.file_uploader(
            "Recipe image (optional)",
            type=["jpg", "jpeg", "png", "webp"],
        )

        submit = st.form_submit_button("Create recipe", use_container_width=True)

    if submit:
        if not title.strip() or not ingredients.strip() or not instructions.strip():
            st.error("Title, ingredients and instructions are required.")
            return

        category_id = None
        if category_name != "Uncategorized":
            category_id = next(
                c["id"] for c in categories if c["name"] == category_name
            )

        try:
            recipe = request(
                "POST",
                "/recipes",
                st.session_state.token,
                json={
                    "title": title,
                    "description": description,
                    "ingredients": ingredients,
                    "instructions": instructions,
                    "prep_time": prep,
                    "cook_time": cook,
                    "servings": servings,
                    "category_id": category_id,
                },
            )

            if image:
                request(
                    "POST",
                    f"/recipes/{recipe['id']}/image",
                    st.session_state.token,
                    files={"file": (image.name, image.getvalue(), image.type)},
                )

            st.success("Recipe created successfully!")
        except Exception as e:
            error_box(e)


def categories_page():
    st.title("🗂️ Categories")

    try:
        categories = get_categories()
    except Exception as e:
        error_box(e)
        return

    with st.form("new_category"):
        name = st.text_input("Category name")
        description = st.text_input("Description")
        submit = st.form_submit_button("Add category")

    if submit:
        try:
            request(
                "POST",
                "/categories",
                st.session_state.token,
                json={"name": name, "description": description},
            )
            st.success("Category created.")
            st.rerun()
        except Exception as e:
            error_box(e)

    st.divider()

    for category in categories:
        with st.container(border=True):
            st.subheader(category["name"])
            st.caption(category.get("description", ""))

            c1, c2 = st.columns(2)

            with c1:
                if st.button("Edit", key=f"edit_cat_{category['id']}"):
                    st.session_state.edit_category = category["id"]
                    st.rerun()

            with c2:
                if st.button("Delete", key=f"del_cat_{category['id']}"):
                    try:
                        request(
                            "DELETE",
                            f"/categories/{category['id']}",
                            st.session_state.token,
                        )
                        st.rerun()
                    except Exception as e:
                        error_box(e)

            if st.session_state.get("edit_category") == category["id"]:
                with st.form(f"edit_cat_form_{category['id']}"):
                    new_name = st.text_input("Name", category["name"])
                    new_desc = st.text_input(
                        "Description",
                        category.get("description", ""),
                    )
                    save = st.form_submit_button("Save")
                if save:
                    try:
                        request(
                            "PUT",
                            f"/categories/{category['id']}",
                            st.session_state.token,
                            json={"name": new_name, "description": new_desc},
                        )
                        st.session_state.pop("edit_category", None)
                        st.rerun()
                    except Exception as e:
                        error_box(e)


if not st.session_state.token:
    login_screen()
    st.stop()

sidebar()

page = st.session_state.page

if page == "Dashboard":
    dashboard()
elif page == "Recipes":
    recipes_page()
elif page == "Favorites":
    recipes_page(True)
elif page == "Add Recipe":
    add_recipe()
elif page == "Categories":
    categories_page()
elif page == "Recipe":
    recipe_page(st.session_state.selected_recipe)
