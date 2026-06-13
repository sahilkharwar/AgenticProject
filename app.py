import streamlit as st

# ==========================
# START SCHEDULER ONCE
# ==========================

if "scheduler_started" not in st.session_state:
    import scheduler
    st.session_state["scheduler_started"] = True

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Health Monitoring System",
    page_icon="🏥",
    layout="wide"
)

# ==========================
# GLOBAL UI STYLING
# ==========================

st.markdown(
    """
<style>

/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F172A,
        #111827
    );
}

/* ALL NAV ITEMS */

[data-testid="stSidebarNav"] * {
    color: white !important;
    opacity: 1 !important;
}

/* NAVIGATION LINKS */

[data-testid="stSidebarNav"] a {
    border-radius: 12px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
    color: white !important;
}

/* HOVER */

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.08);
}

/* ACTIVE PAGE */

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* KEEP ICONS + TEXT WHITE */

[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a p,
[data-testid="stSidebarNav"] a div {
    color: white !important;
    opacity: 1 !important;
}

/* ==========================
   LOGOUT BUTTON
========================== */

[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(
        135deg,
        #DC143C,
        #DC2626
    );
    color: white;
    border: none;
    border-radius: 12px;
    height: 45px;
    font-weight: 600;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #B91C1C;
    color: white;
}

/* ==========================
   MAIN AREA
========================== */

.main {
    background: linear-gradient(
        135deg,
        #F0FDF4 0%,
        #ECFDF5 50%,
        #EFF6FF 100%
    );
}

/* ==========================
   METRIC CONTAINERS
========================== */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    padding: 15px;
}

</style>
""",
    unsafe_allow_html=True
)

# ==========================
# PUBLIC PAGES
# ==========================

login_page = st.Page(
    "pages/Login.py",
    title="Login",
    icon="🔑",
    default=True
)

signup_page = st.Page(
    "pages/Signup.py",
    title="Signup",
    icon="📝"
)

# ==========================
# PRIVATE PAGES
# ==========================

dashboard_page = st.Page(
    "pages/Dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

profile_page = st.Page(
    "pages/User.py",
    title="Profile",
    icon="👤"
)

medication_page = st.Page(
    "pages/Medication.py",
    title="Medication",
    icon="💊"
)

fitness_page = st.Page(
    "pages/Fitness.py",
    title="Fitness",
    icon="🏃"
)

ai_page = st.Page(
    "pages/AI_assitant.py",
    title="AI Assistant",
    icon="🤖"
)

reports_page = st.Page(
    "pages/Reports.py",
    title="Reports",
    icon="📊"
)

# ==========================
# AUTHENTICATED NAVIGATION
# ==========================

if st.session_state.get("logged_in"):

    username = st.session_state.get(
        "username",
        "User"
    )

    st.sidebar.markdown(
        f"""
        <div style="
            background:rgba(16,185,129,0.15);
            padding:15px;
            border-radius:15px;
            text-align:center;
            margin-bottom:15px;
            color:white;
            font-weight:600;
            font-size:16px;
        ">
            👤 {username}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.rerun()

    pg = st.navigation(
        [
            dashboard_page,
            profile_page,
            medication_page,
            fitness_page,
            ai_page,
            reports_page
        ]
    )

# ==========================
# PUBLIC NAVIGATION
# ==========================

else:

    pg = st.navigation(
        [
            login_page,
            signup_page
        ],
        position="hidden"
    )

# ==========================
# RUN APP
# ==========================

pg.run()