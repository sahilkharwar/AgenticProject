import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

from Models.User import (
    get_user,
    update_profile,
    delete_user
)

user = get_user(
    st.session_state["user_id"]
)

st.title("👤 My Profile")

# ==========================
# USER INFO
# ==========================

st.text_input(
    "Username",
    value=user.get("username", ""),
    disabled=True
)

st.text_input(
    "Email",
    value=user.get("email", ""),
    disabled=True
)

st.divider()

# ==========================
# PROFILE DETAILS
# ==========================

age = st.number_input(
    "Age",
    min_value=0,
    max_value=120,
    value=int(
        user.get(
            "age",
            0
        )
    )
)

col1, col2 = st.columns(2)

with col1:

    height_feet = st.number_input(
        "Height (Feet)",
        min_value=0,
        max_value=8,
        value=int(
            user.get(
                "height_feet",
                0
            )
        )
    )

with col2:

    height_inches = st.number_input(
        "Height (Inches)",
        min_value=0,
        max_value=11,
        value=int(
            user.get(
                "height_inches",
                0
            )
        )
    )

weight = st.number_input(
    "Weight (kg)",
    min_value=0.0,
    value=float(
        user.get(
            "weight",
            0
        )
    )
)

# ==========================
# BMI PREVIEW
# ==========================

total_inches = (
    height_feet * 12
) + height_inches

height_meters = (
    total_inches * 2.54
) / 100

bmi = 0

if height_meters > 0:

    bmi = round(
        weight /
        (
            height_meters ** 2
        ),
        1
    )

st.metric(
    "⚖️ BMI",
    bmi
)

# ==========================
# ACTION BUTTONS
# ==========================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "💾 Update Profile",
        use_container_width=True
    ):

        if age <= 0:

            st.error(
                "Age must be greater than 0"
            )

        elif height_feet <= 0:

            st.error(
                "Height must be greater than 0"
            )

        elif height_inches < 0:

            st.error(
                "Height inches cannot be negative"
            )

        elif weight <= 0:

            st.error(
                "Weight must be greater than 0"
            )

        else:

            update_profile(
                st.session_state["user_id"],
                age,
                height_feet,
                height_inches,
                weight
            )

            st.success(
                "Profile Updated Successfully"
            )

            st.rerun()

with col2:

    if st.button(
        "🗑️ Delete Account",
        use_container_width=True
    ):

        delete_user(
            st.session_state["user_id"]
        )

        st.session_state.clear()

        st.success(
            "Account Deleted Successfully"
        )

        st.rerun()