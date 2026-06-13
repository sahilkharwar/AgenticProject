import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from Models.health import (
    calculate_health_assessment
)
from database import (
    fitness_collection,
    med_collection
)

from Models.User import (
    get_user
)

from Models.fitness import (
    get_fitness_streak,
    get_daily_goal
)

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
}

[data-testid="stSidebar"] *{
    color:white;
}

.health-logo{
    text-align:center;
    padding:10px;
}

.health-logo h1{
    color:white;
    margin-bottom:0;
}

.health-logo p{
    color:#CBD5E1;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

[data-testid="metric-container"]{
background:linear-gradient(
    135deg,
    #2563EB,
    #4F46E5
);
color:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 6px 20px rgba(0,0,0,0.08);
    border:none;
}

[data-testid="metric-container"] label{
    font-size:14px;
}

            
</style>
""", unsafe_allow_html=True)



# ==========================
# AUTHENTICATION CHECK
# ==========================

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# ==========================
# FETCH USER DATA
# ==========================

user_id = st.session_state["user_id"]

profile = get_user(
    user_id
)

fitness_data = list(
    fitness_collection.find(
        {
            "user_id": user_id
        }
    )
)

meds = list(
    med_collection.find(
        {
            "user_id": user_id
        }
    )
)

# ==========================
# HERO SECTION
# ==========================

st.markdown(
    f"""
<div style="
background:linear-gradient(
    135deg,
    #2563EB,
    #4F46E5
);
color:white;
padding:25px;
border-radius:20px;
margin-bottom:20px;
box-shadow:0px 2px 10px rgba(0,0,0,0.05);
">

<h1 style="
font-size:48px;
font-weight:800;
margin:0;
padding-top:10px;
line-height:1.3;
color:white;
">
Good Morning, {st.session_state.get('username','User')} 👋
</h1>

<p style="
font-size:18px;
color:rgba(255,255,255,0.85);
">
Here's your health overview for today
</p>

</div>
""",
    unsafe_allow_html=True
)

# ==========================
# BMI CALCULATION
# ==========================

weight = profile.get(
    "weight",
    0
)

height_feet = profile.get(
    "height_feet",
    0
)

height_inches = profile.get(
    "height_inches",
    0
)

total_inches = (
    height_feet * 12
) + height_inches

height_meters = (
    total_inches * 2.54
) / 100

bmi = 0

if height_meters > 0 and weight > 0:

    bmi = round(
        weight /
        (
            height_meters ** 2
        ),
        1
    )

# ==========================
# METRICS
# ==========================

total_activity = sum(
    item.get(
        "value",
        0
    )
    for item in fitness_data
)

total_calories = sum(
    item.get(
        "calories",
        0
    )
    for item in fitness_data
)

total_medications = len(
    meds
)

# ==========================
# GOAL PROGRESS
# ==========================

daily_goal = get_daily_goal(
    user_id
)

today = pd.Timestamp.now().date()

today_steps = sum(

    item.get(
        "value",
        0
    )

    for item in fitness_data

    if (
        item.get("unit") == "steps"
        and
        item.get("date")
        and item.get("date").date() == today
    )
)

goal_progress = 0

if daily_goal > 0:

    goal_progress = round(
        (
            today_steps /
            daily_goal
        ) * 100,
        1
    )

goal_progress = min(
    goal_progress,
    100
)

streak = get_fitness_streak(
    user_id
)

# ==========================
# HEALTH SCORE
# ==========================

assessment = calculate_health_assessment(
    bmi,
    total_calories,
    goal_progress
)

health_score = assessment[
    "health_score"
]

health_risk = assessment[
    "health_risk"
]

recommendation = assessment[
    "recommendation"
]

score_breakdown = assessment[
    "score_breakdown"
]






most_active = "N/A"

if fitness_data:

    activity_counts = {}

    for item in fitness_data:

        category = item.get(
            "category",
            "Other"
        )

        activity_counts[
            category
        ] = activity_counts.get(
            category,
            0
        ) + 1

    most_active = max(
        activity_counts,
        key=activity_counts.get
    )

average_calories = 0

if fitness_data:

    average_calories = round(
        total_calories /
        len(fitness_data),
        1
    )

    

# ==========================
# DASHBOARD CARDS
# ==========================

st.markdown("""
<style>

.metric-card{
    background:linear-gradient(
        135deg,
        #2563EB,
        #4F46E5
    );
    padding:20px;
    border-radius:18px;
    text-align:center;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.metric-title{
    color:#64748B;
    font-size:14px;
    font-weight:600;
}

.metric-value{
    font-size:32px;
    font-weight:bold;
    color:#0F172A;
}

</style>
""", unsafe_allow_html=True)



# ==========================
# KPI CARDS
# ==========================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "❤️ Health Score",
        f"{health_score}/100"
    )

with metric2:
    st.metric(
        "⚖️ BMI",
        bmi
    )

with metric3:
    st.metric(
        "🔥 Streak",
        streak
    )

with metric4:
    st.metric(
        "🎯 Goal Progress",
        f"{goal_progress}%"
    )
# ==========================
# HEALTH OVERVIEW SECTION
# ==========================

st.divider()

gauge_col, info_col = st.columns([1, 1])

# ----------------------------------
# LEFT SIDE - HEALTH SCORE GAUGE
# ----------------------------------

with gauge_col:

    st.subheader("❤️ Health Score Overview")

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health_score,
            
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#10B981"},
                "steps": [
                    {"range": [0, 60], "color": "#FEE2E2"},
                    {"range": [60, 85], "color": "#FEF3C7"},
                    {"range": [85, 100], "color": "#DCFCE7"}
                ]
            }
        )
    )

    gauge_fig.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=30,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        gauge_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ----------------------------------
# RIGHT SIDE - HEALTH ASSESSMENT
# ----------------------------------

with info_col:

    st.subheader("🩺 Health Assessment")

    if health_score >= 85:
        st.success(f"✅ Health Score: {health_score}/100")
        st.info(f"🟢 Risk Level: {health_risk}")

    elif health_score >= 60:
        st.warning(f"⚠️ Health Score: {health_score}/100")
        st.info(f"🟡 Risk Level: {health_risk}")

    else:
        st.error(f"❌ Health Score: {health_score}/100")
        st.info(f"🔴 Risk Level: {health_risk}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💡 Today's Recommendation")

    st.info(
        recommendation
    )
# ==========================
# GOAL PROGRESS
# ==========================

st.divider()

left_col, right_col = st.columns([2, 1])

# ----------------------------------
# LEFT SIDE
# ----------------------------------

with left_col:

    st.subheader("🎯 Today's Goal Progress")

    st.progress(goal_progress / 100)

    st.success(
        f"{today_steps:,} / {daily_goal:,} Steps Completed ({goal_progress:.0f}%)"
    )

# ----------------------------------
# CALCULATE TODAY CALORIES
# ----------------------------------

today_calories = sum(
    item.get("calories", 0)
    for item in fitness_data
    if (
        item.get("date")
        and item.get("date").date() == today
    )
)

# ----------------------------------
# RIGHT SIDE
# ----------------------------------

with right_col:

    st.subheader("📅 Today's Summary")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "👣 Steps",
            f"{today_steps:,}"
        )

        st.metric(
            "🏆 Activity",
            most_active
        )

    with c2:
        st.metric(
            "🔥 Calories",
            f"{today_calories:,}"
        )

        st.metric(
            "💊 Medications",
            total_medications
        )

    st.metric(
        "📊 Avg Calories",
        round(average_calories, 1)
    )

st.divider()

# ==========================
# HEALTH SCORE BREAKDOWN
# ==========================

st.subheader(
    "📊 Health Score Breakdown"
)

for item in score_breakdown:

    st.write(
        f"✅ {item}"
    )



# ==========================
# ACHIEVEMENTS
# ==========================

st.subheader(
    "🏆 Achievement Summary"
)

achievements = []

if len(fitness_data) >= 1:

    achievements.append(
        "🏅 First Activity Logged"
    )

if total_calories >= 1000:

    achievements.append(
        "🔥 Burned 1000 Calories"
    )

if streak >= 7:

    achievements.append(
        "🏆 7 Day Streak"
    )

if goal_progress >= 100:

    achievements.append(
        "🎯 Goal Achieved Today"
    )

if achievements:

    for achievement in achievements:

        st.success(
            achievement
        )

else:

    st.info(
        "No achievements unlocked yet."
    )

# ==========================
# HEALTH ALERTS
# ==========================

alerts = []

if bmi >= 25:

    alerts.append(
        "⚠️ BMI is above healthy range."
    )

if len(
    fitness_data
) == 0:

    alerts.append(
        "⚠️ No fitness activity recorded."
    )

if len(
    meds
) == 0:

    alerts.append(
        "⚠️ No medications added."
    )

if alerts:

    st.warning(
        "\n\n".join(alerts)
    )

# ==========================
# ACTIVITY DISTRIBUTION
# ==========================

activity_counts = {}

for item in fitness_data:

    category = item.get(
        "category",
        "Other"
    )

    activity_counts[
        category
    ] = activity_counts.get(
        category,
        0
    ) + 1

if activity_counts:

    st.subheader(
        "🏆 Activity Distribution"
    )

    summary_df = pd.DataFrame(
        {
            "Activity":
            activity_counts.keys(),

            "Count":
            activity_counts.values()
        }
    )

    fig = px.pie(
        summary_df,
        names="Activity",
        values="Count",
        title="Workout Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# FITNESS ANALYTICS
# ==========================

st.subheader(
    "📈 Fitness Analytics"
)

if fitness_data:

    df = pd.DataFrame(
        fitness_data
    )

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"]
        )

        category_options = [
            "All"
        ]

        if "category" in df.columns:

            category_options += sorted(
                df["category"]
                .dropna()
                .unique()
                .tolist()
            )

        col1, col2 = st.columns(2)

        with col1:

            selected_view = st.selectbox(
                "View By",
                [
                    "Daily",
                    "Monthly",
                    "Yearly"
                ]
            )

        with col2:

            selected_category = st.selectbox(
                "Activity",
                category_options
            )

        filtered_df = df.copy()

        if (
            selected_category != "All"
            and "category" in filtered_df.columns
        ):

            filtered_df = filtered_df[
                filtered_df["category"]
                ==
                selected_category
            ]

        if selected_view == "Daily":

            filtered_df["period"] = (
                filtered_df["date"]
                .dt.strftime(
                    "%Y-%m-%d"
                )
            )

        elif selected_view == "Monthly":

            filtered_df["period"] = (
                filtered_df["date"]
                .dt.strftime(
                    "%Y-%m"
                )
            )

        else:

            filtered_df["period"] = (
                filtered_df["date"]
                .dt.strftime(
                    "%Y"
                )
            )

        chart_data = (
            filtered_df
            .groupby("period")
            .agg(
                {
                    "value": "sum",
                    "calories": "sum"
                }
            )
            .reset_index()
        )

        metric_choice = st.radio(
            "Metric",
            [
                "Activity",
                "Calories"
            ],
            horizontal=True
        )

        y_column = (
            "value"
            if metric_choice == "Activity"
            else "calories"
        )

        fig = px.line(
            chart_data,
            x="period",
            y=y_column,
            markers=True,
            title=f"{metric_choice} Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "No fitness data available."
    )

# ==========================
# RECENT FITNESS RECORDS
# ==========================

st.subheader(
    "🏃 Recent Fitness Records"
)

if fitness_data:

    for item in reversed(
        fitness_data
    ):

        date_text = ""

        if "date" in item:

            try:

                date_text = (
                    item["date"]
                    .strftime(
                        "%d-%m-%Y"
                    )
                )

            except:

                pass

        with st.expander(
            f"{item.get('category')} • {item.get('value')} {item.get('unit')}"
        ):

            st.write(
                f"🔥 Calories: {item.get('calories',0)}"
            )

            st.write(
                f"📅 Date: {date_text}"
            )

else:

    st.info(
        "No fitness records available."
    )

# ==========================
# MEDICATIONS
# ==========================

# ==========================
# UPCOMING MEDICATIONS
# ==========================

st.subheader(
    "💊 Medication Overview"
)

pending_meds = [

    med

    for med in meds

    if not med.get(
        "is_taken",
        False
    )
]

taken_meds = [

    med

    for med in meds

    if med.get(
        "is_taken",
        False
    )
]

# ==========================
# PENDING MEDICATIONS
# ==========================

st.markdown(
    "### ⏳ Pending Medications"
)

if pending_meds:

    pending_meds = sorted(
        pending_meds,
        key=lambda x: x.get(
            "time",
            ""
        )
    )

    for med in pending_meds:

        st.warning(
            f"💊 {med.get('medicine')} | {med.get('dosage')} | ⏰ {med.get('time')}"
        )

else:

    st.success(
        "✅ No pending medications."
    )

# ==========================
# TAKEN MEDICATIONS
# ==========================

st.markdown(
    "### ✅ Taken Today"
)

if taken_meds:

    taken_meds = sorted(
        taken_meds,
        key=lambda x: x.get(
            "time",
            ""
        )
    )

    for med in taken_meds:

        st.success(
            f"💊 {med.get('medicine')} | {med.get('dosage')} | ⏰ {med.get('time')}"
        )

else:

    st.info(
        "No medications marked as taken."
    )

# ==========================
# MEDICATION SUMMARY
# ==========================

col1, col2 = st.columns(2)

col1.metric(
    "⏳ Pending",
    len(pending_meds)
)

col2.metric(
    "✅ Taken",
    len(taken_meds)
)