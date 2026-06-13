import streamlit as st
from Models.Auth import register_user

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

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.stApp{
    background:#F1F5F9;
}

.hero-section{
    background:linear-gradient(
        135deg,
        #0F172A,
        #2563EB
    );
    padding:40px;
    border-radius:25px;
    margin-bottom:25px;
}

.hero-title{
    font-size:52px;
    font-weight:800;
    color:white;
}

.hero-subtitle{
    font-size:18px;
    color:#E2E8F0;
    margin-top:10px;
}

.feature-box{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(
        0,
        0,
        0,
        0.06
    );
}

.big-icon{
    font-size:80px;
    text-align:center;
}

.feature{
    color:#334155;
    font-size:17px;
    margin-bottom:14px;
}

.signup-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 10px 25px rgba(
        0,
        0,
        0,
        0.08
    );
    border:1px solid #E2E8F0;
}

.footer{
    text-align:center;
    color:#64748B;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# HERO SECTION
# ==========================

st.markdown("""
<div class="hero-section">

<div class="hero-title">
🏥 Health Monitoring System
</div>

<div class="hero-subtitle">
Track Fitness • Manage Medications • AI Powered Healthcare Insights
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
    🏥
    </div>

    <h2>
    Everything You Need For Better Health
    </h2>

    <br>

    <div class="feature">
    ✅ AI Health Assistant
    </div>

    <div class="feature">
    ✅ Fitness Tracking
    </div>

    <div class="feature">
    ✅ Medication Management
    </div>

    <div class="feature">
    ✅ Health Analytics
    </div>

    <div class="feature">
    ✅ Smart PDF Reports
    </div>

    <div class="feature">
    ✅ Personalized Insights
    </div>

    </div>
    """, unsafe_allow_html=True)

# ==========================
# RIGHT PANEL
# ==========================

with right_col:

    st.markdown("""
    <div class="signup-card">

    <h1>
    🚀 Create Account
    </h1>

    <p style="color:#64748B;">
    Start tracking your health smarter today.
    </p>

    </div>
    """, unsafe_allow_html=True)

    username = st.text_input(
        "👤 Username"
    )

    email = st.text_input(
        "📧 Email Address"
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    confirm_password = st.text_input(
        "🔐 Confirm Password",
        type="password"
    )

    st.caption(
        "By creating an account you agree to use the platform responsibly."
    )

    # ==========================
    # PASSWORD STRENGTH
    # ==========================

    if password:

        if len(password) < 8:

            st.error(
                "Weak Password"
            )

        elif len(password) < 12:

            st.warning(
                "Medium Password"
            )

        else:

            st.success(
                "Strong Password"
            )

    if st.button(
        "🚀 Create Account",
        use_container_width=True
    ):

        if not username.strip():

            st.error(
                "Username is required"
            )

        elif not email.strip():

            st.error(
                "Email is required"
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match"
            )

        else:

            success = register_user(
                username,
                email,
                password
            )

            if success:

                st.success(
                    "Account Created Successfully"
                )

                st.switch_page(
                    "pages/Login.py"
                )

            else:

                st.error(
                    "Email already exists"
                )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "Already have an account?"
    )

    if st.button(
        "🔑 Login",
        use_container_width=True
    ):
        st.switch_page(
            "pages/Login.py"
        )

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    🏥 Health Monitoring System • Team Nexor • 2026
    </div>
    """,
    unsafe_allow_html=True
)