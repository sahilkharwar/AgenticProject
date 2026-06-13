import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

from AI.assistant import ask_health_assistant
from Models.health import (
    calculate_health_assessment
)
from Models.User import get_user
from Models.fitness import (
    get_fitness_data,
    get_fitness_streak,
    get_daily_goal
)
from Models.medication import get_medications

from Models.chat import (
    create_chat,
    save_message,
    get_user_chats,
    get_chat,
    delete_chat,
    update_chat_title
)

from Utils.report_generator import (
    create_health_report
)

# ==========================
# LOAD USER DATA
# ==========================

profile = get_user(
    st.session_state["user_id"]
)

fitness_data = get_fitness_data(
    st.session_state["user_id"]
)

medications = get_medications(
    st.session_state["user_id"]
)

# ==========================
# CURRENT CHAT
# ==========================

if "current_chat_id" not in st.session_state:
    st.session_state["current_chat_id"] = None

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.markdown(
            """
        ### 🤖 AI Assistant

        Ask health questions,
        review fitness trends,
        analyze medications,
        and generate reports.
        """
    )

    st.divider()

    st.subheader("💬 Chat History")

    


    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state[
            "current_chat_id"
        ] = None

        st.rerun()

    st.divider()

    chats = [
        chat
        for chat in get_user_chats(
            st.session_state["user_id"]
        )
        if len(
            chat.get(
                "messages",
                []
            )
        ) > 0
    ]

    for chat in chats:

        col1, col2 = st.columns(
            [5, 1]
        )

        title = chat.get(
            "title",
            "Untitled Chat"
        )

        if len(title) > 25:
            title = title[:25] + "..."

        with col1:

            if st.button(
                title,
                key=f"chat_{chat['_id']}",
                use_container_width=True
            ):

                st.session_state[
                    "current_chat_id"
                ] = str(chat["_id"])

                st.rerun()

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{chat['_id']}"
            ):

                delete_chat(
                    str(chat["_id"])
                )

                if (
                    st.session_state[
                        "current_chat_id"
                    ]
                    ==
                    str(chat["_id"])
                ):

                    st.session_state[
                        "current_chat_id"
                    ] = None

                st.rerun()

# ==========================
# PAGE TITLE
# ==========================

st.markdown(
    f"""
<div style="
background:white;
padding:25px;
border-radius:20px;
margin-bottom:20px;
box-shadow:0px 2px 10px rgba(0,0,0,0.05);
">

<h1>
🤖 AI Health Assistant
</h1>

<p style="color:#64748B;font-size:18px;">
Personalized AI-powered healthcare insights for {st.session_state.get('username','User')}
</p>

</div>
""",
    unsafe_allow_html=True
)



# ==========================
# QUICK ACTIONS
# ==========================

st.subheader(
    "⚡ Quick Actions"
)


action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(5)

with action_col1:

    bmi_btn = st.button(
        "⚖️ BMI Analysis",
        use_container_width=True
    )

with action_col2:

    summary_btn = st.button(
        "📊 Health Summary",
        use_container_width=True
    )

with action_col3:

    fitness_btn = st.button(
        "🏃 Fitness Insights",
        use_container_width=True
    )

with action_col4:

    med_btn = st.button(
        "💊 Medication Review",
        use_container_width=True
    )

with action_col5:

    report_btn = st.button(
        "📄 Health Report",
        use_container_width=True
    )

# ==========================
# HEALTH CARDS
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

total_activities = len(
    fitness_data
)

total_medications = len(
    medications
)

# ==========================
# AI HEALTH DATA
# ==========================

daily_goal = get_daily_goal(
    st.session_state["user_id"]
)

streak = get_fitness_streak(
    st.session_state["user_id"]
)

from datetime import datetime

today = datetime.now().date()

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
        and
        item.get("date").date() == today
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

# ==========================
# HEALTH ASSESSMENT
# ==========================

total_calories = sum(
    item.get(
        "calories",
        0
    )
    for item in fitness_data
)

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

achievements = []

if len(fitness_data) >= 1:

    achievements.append(
        "First Activity Logged"
    )

if total_calories >= 1000:

    achievements.append(
        "Burned 1000 Calories"
    )

if streak >= 7:

    achievements.append(
        "7 Day Streak"
    )

if goal_progress >= 100:

    achievements.append(
        "Goal Achieved"
    )

card1, card2, card3, card4, card5 = st.columns(5)

card1.metric(
    "❤️ Health Score",
    f"{health_score}/100"
)

card2.metric(
    "⚖️ BMI",
    bmi
)

card3.metric(
    "🔥 Streak",
    streak
)

card4.metric(
    "🎯 Goal",
    f"{goal_progress}%"
)

card5.metric(
    "💊 Medications",
    total_medications
)

# ==========================
# AI HEALTH SNAPSHOT
# ==========================

st.success(
    f"""
### 🤖 AI Health Snapshot

❤️ Health Score: {health_score}/100

🔥 Current Streak: {streak} Days

🎯 Goal Progress: {goal_progress}%

⚠️ Risk Level: {health_risk}
"""
)

st.divider()

# ==========================
# LOAD CHAT
# ==========================

messages = []

if st.session_state["current_chat_id"]:

    chat = get_chat(
        st.session_state["current_chat_id"]
    )

    if chat:

        messages = chat.get(
            "messages",
            []
        )

# ==========================
# DISPLAY CHAT
# ==========================

for message in messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# ==========================
# QUESTION SOURCE
# ==========================

question = None

if bmi_btn:

    question = (
        "Calculate my BMI and explain whether it is healthy."
    )

elif summary_btn:

    question = (
        "Generate a complete health summary."
    )

elif fitness_btn:

    question = (
        "Analyze my fitness activities and provide recommendations."
    )

elif med_btn:

    question = (
        "Review my medications and provide useful information."
    )

elif report_btn:

    question = """
Generate a professional health report.

Include:

- Profile Summary
- BMI Analysis
- Fitness Summary
- Medication Summary
- Personalized Recommendations

Format the response as a professional report.
"""

else:

    question = st.chat_input(
        "Ask me anything about your health..."
    )

# ==========================
# PROCESS QUESTION
# ==========================

if question:

    if st.session_state["current_chat_id"] is None:

        chat_id = create_chat(
            st.session_state["user_id"],
            question[:30]
        )

        st.session_state[
            "current_chat_id"
        ] = chat_id

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    save_message(
        st.session_state["current_chat_id"],
        "user",
        question
    )

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing your health data..."
        ):

           answer = ask_health_assistant(
                profile,
                fitness_data,
                medications,
                messages,
                question,
                health_score,
                streak,
                daily_goal,
                goal_progress,
                today_steps,
                achievements,
                health_risk,
                recommendation,
                score_breakdown
            )

        response_placeholder = st.empty()

        full_response = ""

        for word in answer.split():

            full_response += (
                word + " "
            )

            response_placeholder.markdown(
                full_response + "▌"
            )

        response_placeholder.markdown(
            full_response
        )

        # ==========================
        # REPORT DOWNLOAD
        # ==========================

        if report_btn:

            pdf_file = create_health_report(
                answer
            )

            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(
                    label="📥 Download Health Report",
                    data=file,
                    file_name="Health_Report.pdf",
                    mime="application/pdf"
                )

    save_message(
        st.session_state["current_chat_id"],
        "assistant",
        answer
    )

    chat = get_chat(
        st.session_state["current_chat_id"]
    )

    if (
        chat
        and
        len(chat.get("messages", [])) <= 2
    ):

        update_chat_title(
            st.session_state["current_chat_id"],
            question[:30]
        )

    st.rerun()