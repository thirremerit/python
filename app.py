
import streamlit as st
import folium
from streamlit_folium import st_folium
import database
import os
import uuid


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="CityCare",
    page_icon="🏙️",
    layout="wide"
)

database.create_tables()


# ---------------- SESSION STATE ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "selected_location" not in st.session_state:
    st.session_state.selected_location = None


# ---------------- NAVIGATION ----------------

def go_to_dashboard():
    role = st.session_state.user["role"]

    if role == "admin":
        st.session_state.page = "admin"

    elif role == "government":
        st.session_state.page = "worker"

    else:
        st.session_state.page = "home"


# ---------------- HEADER ----------------

def show_header():
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title("🏙️ CityCare")
        st.caption("Your city, your voice.")

    with col2:
        st.write("")
        st.write("")

        if st.session_state.user:
            if st.button("Log Out", use_container_width=True):
                st.session_state.user = None
                st.session_state.page = "login"
                st.session_state.selected_location = None
                st.rerun()

        else:
            if st.button("Log In", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

    st.divider()


# ---------------- LOGIN ----------------

def show_login():
    st.title("🏙️ CityCare")
    st.subheader("Your city, your voice.")

    st.divider()

    st.header("Welcome Back")
    st.write("Log in to continue to CityCare.")

    with st.form("login_form"):
        identifier = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            "Log In",
            use_container_width=True
        )

        if submitted:
            user = database.login_user(
                identifier.strip(),
                password
            )

            if user:
                st.session_state.user = user
                go_to_dashboard()
                st.rerun()

            else:
                st.error("Incorrect username/email or password.")

    st.write("Don't have an account?")

    if st.button("Create an Account", use_container_width=True):
        st.session_state.page = "signup"
        st.rerun()

    st.divider()

    if st.button("Continue as Guest", use_container_width=True):
        st.session_state.page = "reports"
        st.rerun()


# ---------------- SIGN UP ----------------

def show_signup():
    st.title("🏙️ CityCare")
    st.subheader("Create your CityCare account.")

    st.divider()

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:
            if not username.strip() or not email.strip() or not password:
                st.error("Please fill in all fields.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")

            elif len(password) < 8:
                st.error("Password must have at least 8 characters.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:
                success, message = database.create_user(
                    username.strip(),
                    email.strip(),
                    password
                )

                if success:
                    st.success("Account created successfully!")
                    st.session_state.page = "login"
                    st.rerun()

                else:
                    st.error(message)

    if st.button("Already have an account? Log In"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- CITIZEN HOME ----------------

def show_home():
    show_header()

    user = st.session_state.user

    st.header(f"Welcome, {user['username']}!")

    st.write(
        "Help make Prishtina a better place by reporting "
        "problems in your community."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Report a Problem")

        st.write(
            "Report potholes, garbage, broken streetlights "
            "and other problems."
        )

        if st.button("Report a Problem", use_container_width=True):
            st.session_state.page = "report"
            st.session_state.selected_location = None
            st.rerun()

    with col2:
        st.subheader("🗺️ Explore the City")

        st.write("See problems reported by the community.")

        if st.button("View Reports", use_container_width=True):
            st.session_state.page = "reports"
            st.rerun()


# ---------------- ADMIN DASHBOARD ----------------

def show_admin_dashboard():
    show_header()

    st.header("🛡️ Administrator Dashboard")

    st.write(
        f"Welcome, {st.session_state.user['username']}!"
    )

    reports = database.get_all_reports()
    workers = database.get_workers()

    pending = sum(
        1 for report in reports
        if report["status"] == "Pending"
    )

    in_progress = sum(
        1 for report in reports
        if report["status"] == "In Progress"
    )

    resolved = sum(
        1 for report in reports
        if report["status"] == "Resolved"
    )

    st.subheader("CityCare Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reports", len(reports))
    col2.metric("Pending", pending)
    col3.metric("In Progress", in_progress)
    col4.metric("Resolved", resolved)

    st.divider()

    # CREATE GOVERNMENT WORKER

    st.subheader("👮 Create Government Worker Account")

    st.write(
        "Create accounts for employees who will manage "
        "community reports."
    )

    with st.form("create_worker_form"):
        username = st.text_input("Worker Username")
        email = st.text_input("Worker Email")
        password = st.text_input(
            "Worker Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Worker Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Worker Account",
            use_container_width=True
        )

        if submitted:
            if not username.strip() or not email.strip() or not password:
                st.error("Please fill in all fields.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")

            elif len(password) < 8:
                st.error("Password must have at least 8 characters.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:
                success, message = database.create_worker(
                    username.strip(),
                    email.strip(),
                    password
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)

    st.divider()

    # WORKER LIST

    st.subheader(f"👥 Government Workers ({len(workers)})")

    if workers:
        for worker in workers:
            with st.container(border=True):
                st.write(f"**Username:** {worker['username']}")
                st.write(f"**Email:** {worker['email']}")

    else:
        st.info("No government workers have been created yet.")

    st.divider()

    if st.button("View All Community Reports", use_container_width=True):
        st.session_state.page = "reports"
        st.rerun()


# ---------------- GOVERNMENT WORKER DASHBOARD ----------------

def show_worker_dashboard():
    show_header()

    st.header("🏛️ Government Worker Dashboard")

    st.write(
        f"Welcome, {st.session_state.user['username']}!"
    )

    st.write(
        "View community problems and update their progress."
    )

    reports = database.get_all_reports()

    pending = sum(
        1 for report in reports
        if report["status"] == "Pending"
    )

    in_progress = sum(
        1 for report in reports
        if report["status"] == "In Progress"
    )

    resolved = sum(
        1 for report in reports
        if report["status"] == "Resolved"
    )

    st.divider()

    st.subheader("Report Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reports", len(reports))
    col2.metric("Pending", pending)
    col3.metric("In Progress", in_progress)
    col4.metric("Resolved", resolved)

    st.divider()

    st.subheader("📋 Manage Community Reports")

    if not reports:
        st.info("There are no reports to manage yet.")
        return

    for report in reports:
        with st.expander(
            f"#{report['id']} - {report['title']} | {report['status']}"
        ):
            st.write("**Category:**", report["category"])
            st.write("**Description:**", report["description"])
            st.write(
                "**Reported by:**",
                report["reported_by"] or "Unknown"
            )
            st.write("**Date:**", report["created_at"])

            st.write(
                "**Location:**",
                f"{report['latitude']:.5f}, "
                f"{report['longitude']:.5f}"
            )

            image_path = report.get("image_path")

            if image_path:
                if os.path.exists(image_path):
                    st.image(
                        image_path,
                        caption="Photo of reported problem",
                        width=400
                    )
                else:
                    st.warning("The uploaded photo could not be found.")

            st.divider()

            st.write("**Update Report Status**")

            statuses = [
                "Pending",
                "In Progress",
                "Resolved"
            ]

            current_status = report["status"]

            if current_status not in statuses:
                current_status = "Pending"

            with st.form(f"status_form_{report['id']}"):
                new_status = st.selectbox(
                    "Select new status",
                    statuses,
                    index=statuses.index(current_status)
                )

                submitted = st.form_submit_button(
                    "Update Status",
                    use_container_width=True
                )

                if submitted:
                    database.update_report_status(
                        report["id"],
                        new_status
                    )

                    st.success("Report status updated!")
                    st.rerun()


# ---------------- REPORT A PROBLEM ----------------

def show_report_page():
    show_header()

    st.header("📍 Report a Problem")

    st.write(
        "Fill in the information below and select the location "
        "of the problem on the map."
    )

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    title = st.text_input(
        "Problem Title",
        placeholder="Example: Large pothole on the road"
    )

    category = st.selectbox(
        "Problem Category",
        [
            "Road Damage",
            "Garbage",
            "Broken Streetlight",
            "Water Problem",
            "Public Property Damage",
            "Other"
        ]
    )

    description = st.text_area(
        "Description",
        placeholder="Describe the problem and where it is..."
    )

    # PHOTO UPLOAD

    st.subheader("📷 Add a Photo")

    uploaded_image = st.file_uploader(
        "Upload a Photo (Optional)",
        type=["jpg", "jpeg", "png"],
        help="Upload a picture showing the reported problem."
    )

    if uploaded_image:
        st.image(
            uploaded_image,
            caption="Photo of the reported problem",
            width=350
        )

    st.divider()

    # LOCATION SELECTION

    st.subheader("🗺️ Select the Problem Location")

    st.write(
        "Click on the map to place a marker where the problem is."
    )

    city_map = folium.Map(
        location=[42.6629, 21.1655],
        zoom_start=14
    )

    if st.session_state.selected_location:
        lat, lon = st.session_state.selected_location

        folium.Marker(
            [lat, lon],
            popup="Selected Problem Location",
            tooltip="Selected Location",
            icon=folium.Icon(color="red")
        ).add_to(city_map)

    map_data = st_folium(
        city_map,
        width=None,
        height=400,
        key="report_map"
    )

    if map_data and map_data.get("last_clicked"):
        clicked = map_data["last_clicked"]

        new_location = (
            clicked["lat"],
            clicked["lng"]
        )

        if new_location != st.session_state.selected_location:
            st.session_state.selected_location = new_location
            st.rerun()

    if st.session_state.selected_location:
        lat, lon = st.session_state.selected_location

        st.success(
            f"Location selected: {lat:.5f}, {lon:.5f}"
        )

    else:
        st.warning("Please click on the map to select a location.")

    st.divider()

    # SUBMIT REPORT

    if st.button("Submit Report", use_container_width=True):

        if not title.strip():
            st.error("Please enter a problem title.")

        elif not description.strip():
            st.error("Please describe the problem.")

        elif not st.session_state.selected_location:
            st.error("Please select a location on the map.")

        else:
            image_path = None

            if uploaded_image:
                os.makedirs("report_images", exist_ok=True)

                file_extension = uploaded_image.name.rsplit(
                    ".", 1
                )[-1].lower()

                image_filename = (
                    f"{uuid.uuid4().hex}.{file_extension}"
                )

                image_path = os.path.join(
                    "report_images",
                    image_filename
                )

                with open(image_path, "wb") as image_file:
                    image_file.write(uploaded_image.getbuffer())

            lat, lon = st.session_state.selected_location

            report_id = database.create_report(
                title.strip(),
                description.strip(),
                category,
                lat,
                lon,
                st.session_state.user["id"],
                image_path
            )

            st.success(
                f"Report #{report_id} submitted successfully!"
            )

            st.session_state.selected_location = None
            st.session_state.page = "reports"
            st.rerun()


# ---------------- VIEW REPORTS ----------------

def show_reports():
    show_header()

    st.header("🗺️ Community Reports")

    st.write(
        "Here you can see problems reported by people in the community."
    )

    if st.session_state.user:
        if st.button("← Back to Dashboard"):
            go_to_dashboard()
            st.rerun()

    else:
        if st.button("← Back to Login"):
            st.session_state.page = "login"
            st.rerun()

    reports = database.get_all_reports()

    st.divider()

    if not reports:
        st.info("No problems have been reported yet.")
        return

    # MAP

    st.subheader("Map of Reported Problems")

    city_map = folium.Map(
        location=[42.6629, 21.1655],
        zoom_start=13
    )

    for report in reports:
        folium.Marker(
            location=[
                report["latitude"],
                report["longitude"]
            ],
            popup=(
                f'{report["title"]} | '
                f'{report["category"]} | '
                f'{report["status"]}'
            ),
            tooltip=report["title"],
            icon=folium.Icon(color="red")
        ).add_to(city_map)

    st_folium(
        city_map,
        width=None,
        height=450,
        key="reports_map"
    )

    st.divider()

    # REPORT LIST

    st.subheader(f"All Reports ({len(reports)})")

    for report in reports:
        with st.expander(
            f'📍 {report["title"]} — {report["status"]}'
        ):
            st.write("**Category:**", report["category"])
            st.write("**Description:**", report["description"])

            image_path = report.get("image_path")

            if image_path:
                if os.path.exists(image_path):
                    st.image(
                        image_path,
                        caption="Photo of reported problem",
                        width=400
                    )
                else:
                    st.warning(
                        "The uploaded photo could not be found."
                    )

            st.write(
                "**Reported by:**",
                report["reported_by"] or "Unknown"
            )

            st.write("**Date:**", report["created_at"])

            st.write(
                "**Location:**",
                f'{report["latitude"]:.5f}, '
                f'{report["longitude"]:.5f}'
            )


# ---------------- PAGE NAVIGATION ----------------

if st.session_state.page == "login":
    show_login()

elif st.session_state.page == "signup":
    show_signup()

elif st.session_state.page == "home":
    if st.session_state.user and st.session_state.user["role"] == "citizen":
        show_home()
    elif st.session_state.user:
        go_to_dashboard()
        st.rerun()
    else:
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "admin":
    if st.session_state.user and st.session_state.user["role"] == "admin":
        show_admin_dashboard()
    elif st.session_state.user:
        go_to_dashboard()
        st.rerun()
    else:
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "worker":
    if st.session_state.user and st.session_state.user["role"] == "government":
        show_worker_dashboard()
    elif st.session_state.user:
        go_to_dashboard()
        st.rerun()
    else:
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "report":
    if st.session_state.user and st.session_state.user["role"] == "citizen":
        show_report_page()
    elif st.session_state.user:
        go_to_dashboard()
        st.rerun()
    else:
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "reports":
    show_reports()

else:
    st.session_state.page = "login"
    st.rerun()
