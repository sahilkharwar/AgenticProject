import streamlit as st
from Models.Auth import login_user

# ==========================
# PAGE STYLING
# ==========================

st.markdown("""
<style>

[data-testid="stSidebar"]{
    display:none;
}

header{
    visibility:hidden;
}

.stApp{
    background:#F1F5F9;
}

/* HERO */

.hero-section{
    background:linear-gradient(
        135deg,
        #0F172A,
        #2563EB
    );
    padding:50px;
    border-radius:25px;
    margin-bottom:30px;
}

.hero-title{
    font-size:56px;
    font-weight:800;
    color:white !important;
}

.hero-subtitle{
    font-size:20px;
    color:#E2E8F0 !important;
}

/* FEATURE CARD */

.feature-box{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,0.06);
}

.feature{
    color:#334155;
    font-size:17px;
    margin-bottom:15px;
}

/* LOGIN CARD */

.login-card{
    background:white;
    padding:35px;
    border-radius:22px;
    box-shadow:0 10px 25px rgba(0,0,0,0.08);
    border:1px solid #E2E8F0;
}

.big-icon{
    font-size:80px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# HERO
# ==========================

st.markdown("""
<div class="hero-section">

<div class="hero-title">
🏥 Health Monitoring System
</div>

<div class="hero-subtitle">
AI Powered Healthcare Companion
</div>

</div>
""", unsafe_allow_html=True)

# ==========================
# LAYOUT
# ==========================

left_col, right_col = st.columns([1.2,1])

# ==========================
# LEFT PANEL
# ==========================

with left_col:

    st.markdown("""
    <div class="feature-box">

    <div class="big-icon">
    🩺
    </div>

    <h2>
    Why Choose Our Platform?
    </h2>

    <div class="feature">
    ✅ Track Fitness Activities
    </div>

    <div class="feature">
    ✅ Manage Daily Medications
    </div>

    <div class="feature">
    ✅ AI Health Assistant
    </div>

    <div class="feature">
    ✅ Generate Smart Health Reports
    </div>

    <div class="feature">
    ✅ Personalized Health Insights
    </div>

    <div class="feature">
    ✅ Monitor Health Progress
    </div>

    </div>
    """, unsafe_allow_html=True)

# ==========================
# RIGHT PANEL
# ==========================

with right_col:

    st.markdown("""
    <div class="login-card">

    <h1>
    👋 Welcome Back
    </h1>

    <p style="color:#64748B;">
    Sign in to continue your healthcare journey.
    </p>

    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "📧 Email Address"
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button(
        "🚀 Login",
        use_container_width=True
    ):

        user = login_user(
            email,
            password
        )

        if user:

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = str(
                user["_id"]
            )

            st.session_state["username"] = user[
                "username"
            ]

            st.success(
                f"Welcome {user['username']}"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "Don't have an account?"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):
        st.switch_page(
            "pages/Signup.py"
        )

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.caption(
    "Health Monitoring System © 2026"
)