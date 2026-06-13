import streamlit as st
import pandas as pd
import plotly.express as px

from database import fitness_collection
from Models.User import get_user
from Utils.report_generator import (
    create_health_report
)

from Models.health import (
    calculate_health_assessment
)
# ==========================
# AUTH CHECK
# ==========================

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# ==========================
# LOAD DATA
# ==========================

user_id = st.session_state["user_id"]

profile = get_user(user_id)

fitness_data = list(
    fitness_collection.find(
        {
            "user_id": user_id
        }
    )
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
# BMI CATEGORY
# ==========================

bmi_status = "Unknown"

if bmi > 0:

    if bmi < 18.5:

        bmi_status = "Underweight"

    elif bmi < 25:

        bmi_status = "Normal"

    elif bmi < 30:

        bmi_status = "Overweight"

    else:

        bmi_status = "Obese"

# ==========================
# PAGE HEADER
# ==========================

st.title("📊 Health Reports")

st.subheader(
    f"Reports for {st.session_state['username']}"
)

# ==========================
# NO DATA
# ==========================

if not fitness_data:

    st.info(
        "No fitness records available."
    )

    st.stop()

# ==========================
# DATAFRAME
# ==========================

df = pd.DataFrame(
    fitness_data
)

df["date"] = pd.to_datetime(
    df["date"]
)

# ==========================
# FILTERS
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:

    report_type = st.selectbox(
        "Report Type",
        [
            "Daily",
            "Monthly",
            "Yearly"
        ]
    )

with col2:

    category_options = ["All"]

    category_options += sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Activity",
        category_options
    )

with col3:

    start_date = st.date_input(
        "Start Date",
        df["date"].min().date()
    )

with col4:

    end_date = st.date_input(
        "End Date",
        df["date"].max().date()
    )

# ==========================
# CATEGORY FILTER
# ==========================

filtered_df = df.copy()

filtered_df = filtered_df[
    (
        filtered_df["date"].dt.date
        >= start_date
    )
    &
    (
        filtered_df["date"].dt.date
        <= end_date
    )
]

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["category"]
        ==
        selected_category
    ]

# ==========================
# DATE GROUPING
# ==========================

if report_type == "Daily":

    filtered_df["period"] = (
        filtered_df["date"]
        .dt.strftime("%Y-%m-%d")
    )

elif report_type == "Monthly":

    filtered_df["period"] = (
        filtered_df["date"]
        .dt.strftime("%Y-%m")
    )

else:

    filtered_df["period"] = (
        filtered_df["date"]
        .dt.strftime("%Y")
    )

if filtered_df.empty:

    st.warning(
        "No records found for selected filters."
    )

    st.stop()

# ==========================
# AGGREGATION
# ==========================

report_df = (
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

# ==========================
# METRICS
# ==========================

total_activity = int(
    report_df["value"].sum()
)

total_calories = int(
    report_df["calories"].sum()
)

average_activity = round(
    report_df["value"].mean(),
    2
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "⚖️ BMI",
    bmi
)

col2.metric(
    "📏 Height",
    f"{height_feet}' {height_inches}\""
)

col3.metric(
    "🏃 Activity",
    total_activity
)

col4.metric(
    "🔥 Calories",
    total_calories
)

col5.metric(
    "📈 Average",
    average_activity
)

# ==========================
# BMI STATUS
# ==========================

if bmi > 0:

    if bmi_status == "Normal":

        st.success(
            f"✅ BMI Status: {bmi_status}"
        )

    elif bmi_status == "Underweight":

        st.warning(
            f"⚠️ BMI Status: {bmi_status}"
        )

    else:

        st.error(
            f"⚠️ BMI Status: {bmi_status}"
        )


assessment = calculate_health_assessment(
    bmi,
    total_calories,
    0
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

st.subheader(
    "❤️ Health Score"
)

st.progress(
    health_score / 100
)

st.metric(
    "Health Score",
    f"{health_score}/100"
)

st.caption(
    f"Risk Level: {health_risk}"
)

# ==========================
# PERSONAL RECORDS
# ==========================

st.subheader(
    "🏆 Personal Records"
)

if not filtered_df.empty:

    best_activity = int(
        filtered_df["value"].max()
    )

    best_calories = int(
        filtered_df["calories"].max()
    )

else:

    best_activity = 0

    best_calories = 0

col1, col2 = st.columns(2)

col1.metric(
    "🏃 Best Activity",
    best_activity
)

col2.metric(
    "🔥 Highest Calories",
    best_calories
)

# ==========================
# ACTIVITY TREND
# ==========================

st.subheader(
    "📈 Activity Trend"
)

fig = px.line(
    report_df,
    x="period",
    y="value",
    markers=True,
    title="Activity Progress"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# CALORIE TREND
# ==========================

st.subheader(
    "🔥 Calories Trend"
)

fig2 = px.bar(
    report_df,
    x="period",
    y="calories",
    title="Calories Burned"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================
# ACTIVITY DISTRIBUTION
# ==========================

st.subheader(
    "🏆 Activity Distribution"
)

activity_counts = (
    filtered_df["category"]
    .value_counts()
    .reset_index()
)

activity_counts.columns = [
    "Activity",
    "Count"
]

fig3 = px.pie(
    activity_counts,
    names="Activity",
    values="Count"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================
# RAW REPORT DATA
# ==========================

st.subheader(
    "📋 Report Data"
)

st.dataframe(
    report_df,
    use_container_width=True
)

# ==========================
# TOP ACTIVITY
# ==========================

if not filtered_df.empty:

    top_activity = (
        filtered_df["category"]
        .mode()[0]
    )

else:

    top_activity = "N/A"

# ==========================
# AI INSIGHTS
# ==========================

st.success(
    f"""
### Health Summary

• BMI: {bmi}

• BMI Status: {bmi_status}

• Health Score: {health_score}/100

• Most Performed Activity: {top_activity}

• Total Calories Burned: {total_calories}

• Average Activity: {average_activity}

• Best Activity: {best_activity}

• Highest Calories Burned: {best_calories}

### Recommendation

{recommendation} """
)

# ==========================
# PDF REPORT
# ==========================

st.divider()

st.subheader(
    "📄 Export Report"
)

if st.button(
    "Generate PDF Report",
    use_container_width=True
):

    report_text = f"""
HEALTH REPORT

Username: {st.session_state['username']}

BMI: {bmi}

BMI Status: {bmi_status}

Health Score: {health_score}/100

Height: {height_feet}' {height_inches}"

Total Activity: {total_activity}

Total Calories Burned: {total_calories}

Average Activity: {average_activity}

Best Activity: {best_activity}

Highest Calories Burned: {best_calories}

Most Performed Activity: {top_activity}

Risk Level: {health_risk}

Recommendation:
{recommendation}

Report Period:
{start_date} to {end_date}

Generated by AI Health Monitoring System
"""

    pdf_file = create_health_report(
        report_text
    )

    with open(
        pdf_file,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download PDF Report",
            data=file,
            file_name="Health_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )