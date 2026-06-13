import streamlit as st
from datetime import datetime
if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

from Models.fitness import (
    add_fitness_data,
    get_fitness_data,
    delete_fitness_record,
    update_fitness_record,
    get_fitness_streak,
    set_daily_goal,
    get_daily_goal
)

st.title("🏃 Fitness Tracker")

# ==========================
# FITNESS INPUT
# ==========================

category = st.selectbox(
    "Activity Type",
    [
        "Walking",
        "Running",
        "Cycling",
        "Gym",
        "Swimming",
        "Yoga",
        "Other"
    ]
)

if category in ["Walking", "Running"]:

    value = st.number_input(
        "Steps",
        min_value=0
    )

    unit = "steps"

elif category == "Cycling":

    value = st.number_input(
        "Distance (km)",
        min_value=0.0
    )

    unit = "km"

elif category == "Swimming":

    value = st.number_input(
        "Laps",
        min_value=0
    )

    unit = "laps"

elif category in ["Gym", "Yoga"]:

    value = st.number_input(
        "Duration (minutes)",
        min_value=0
    )

    unit = "minutes"

else:

    value = st.number_input(
        "Activity Value",
        min_value=0.0
    )

    unit = "custom"

calories = st.number_input(
    "Calories Burned",
    min_value=0
)

activity_date = st.date_input(
    "Activity Date"
)

if st.button("Save Fitness Data"):

    if value <= 0:

        st.error(
            "Activity value must be greater than 0"
        )

    elif calories < 0:

        st.error(
            "Calories cannot be negative"
        )

    else:

        add_fitness_data(
            st.session_state["user_id"],
            value,
            calories,
            category,
            unit,
            datetime.combine(
                activity_date,
                datetime.min.time()
            )
        )

        st.success(
            "Fitness Data Saved Successfully"
        )

        st.rerun()

    


st.divider()

# ==========================
# LOAD RECORDS
# ==========================

fitness_records = get_fitness_data(
    st.session_state["user_id"]
)

# ==========================
# FITNESS GOAL
# ==========================

current_goal = get_daily_goal(
    st.session_state["user_id"]
)

st.subheader(
    "🎯 Daily Fitness Goal"
)

col1, col2 = st.columns([3, 1])

with col1:

    goal = st.number_input(
        "Daily Goal (Steps)",
        min_value=1000,
        value=current_goal,
        step=500
    )

with col2:

    st.write("")

    if st.button(
        "Save Goal"
    ):

        if goal <= 0:

            st.error(
                "Goal must be greater than 0"
            )

        else:

            set_daily_goal(
                st.session_state["user_id"],
                goal
            )

            st.success(
                "Goal Updated"
            )

            st.rerun()
# ==========================
# GOAL PROGRESS
# ==========================

selected_date = activity_date

today_steps = sum(

    record.get(
        "value",
        0
    )

    for record in fitness_records

    if (
        record.get("unit") == "steps"
        and
        record.get("date").date() == selected_date
    )
)

goal_progress = min(
    (
        today_steps / current_goal
    ) * 100,
    100
)

st.progress(
    goal_progress / 100
)

st.write(
    f"🎯 {today_steps} / {current_goal} Steps on {selected_date} ({goal_progress:.1f}%)"
)


# ==========================
# FITNESS STREAK
# ==========================

streak = get_fitness_streak(
    st.session_state["user_id"]
)

st.metric(
    "🔥 Current Streak",
    f"{streak} Days"
)
# ==========================
# FITNESS STATS
# ==========================

total_calories = 0

if fitness_records:

    total_records = len(
        fitness_records
    )

    total_calories = sum(
        record.get(
            "calories",
            0
        )
        for record in fitness_records
    )

    best_record = max(
        fitness_records,
        key=lambda x: x.get(
            "value",
            0
        )
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏃 Activities",
        total_records
    )

    col2.metric(
        "🔥 Calories",
        total_calories
    )

    col3.metric(
        "🏆 Best Performance",
        f"{best_record.get('value')} {best_record.get('unit')}"
    )

st.divider()

# ==========================
# ACHIEVEMENTS
# ==========================

st.subheader(
    "🏆 Achievements"
)

achievements = []

if len(fitness_records) >= 1:

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

if streak >= 30:

    achievements.append(
        "👑 30 Day Streak"
    )

if goal_progress >= 100:

    achievements.append(
        "🎯 Goal Achieved"
    )

if len(fitness_records) >= 50:

    achievements.append(
        "🏅 50 Activities Completed"
    )

if achievements:

    for badge in achievements:

        st.success(
            badge
        )

else:

    st.info(
        "No achievements unlocked yet."
    )

# ==========================
# RECORDS SECTION
# ==========================

st.subheader(
    "📋 My Fitness Records"
)

if fitness_records:

    categories = ["All"] + sorted(
        list(
            set(
                record.get(
                    "category",
                    "Other"
                )
                for record in fitness_records
            )
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        selected_category = st.selectbox(
            "Filter By Activity",
            categories
        )

    with col2:

        search_text = st.text_input(
            "🔍 Search Activity"
        )

    # ==========================
    # CATEGORY FILTER
    # ==========================

    if selected_category != "All":

        fitness_records = [
            record
            for record in fitness_records
            if record.get(
                "category"
            ) == selected_category
        ]

    # ==========================
    # IMPROVED SEARCH
    # ==========================

    if search_text:

        search_text = search_text.lower()

        fitness_records = [

            record

            for record in fitness_records

            if (
                search_text
                in str(
                    record.get(
                        "category",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    record.get(
                        "unit",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    record.get(
                        "value",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    record.get(
                        "calories",
                        ""
                    )
                ).lower()
            )
        ]

    # ==========================
    # RECORD DISPLAY
    # ==========================

    for record in reversed(
        fitness_records
    ):

        date_text = ""

        if "date" in record:

            try:

                date_text = (
                    record["date"]
                    .strftime(
                        "%d-%m-%Y"
                    )
                )

            except:

                pass

        with st.expander(
            f"{record.get('category')} • {record.get('value')} {record.get('unit')}"
        ):

            st.write(
                f"🔥 Calories: {record.get('calories',0)}"
            )

            st.write(
                f"📅 Date: {date_text}"
            )

            new_value = st.number_input(
                "Update Value",
                value=float(
                    record.get(
                        "value",
                        0
                    )
                ),
                key=f"value_{record['_id']}"
            )

            new_calories = st.number_input(
                "Update Calories",
                value=int(
                    record.get(
                        "calories",
                        0
                    )
                ),
                key=f"calories_{record['_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Save Changes",
                    key=f"save_{record['_id']}"
                ):

                    if new_value <= 0:

                        st.error(
                            "Activity value must be greater than 0"
                        )

                    elif new_calories < 0:

                        st.error(
                        "Calories cannot be negative"
                        )

                    else:

                        update_fitness_record(
                            str(record["_id"]),
                            new_value,
                            new_calories
                        )

                        st.success(
                            "Record Updated Successfully"
                        )

                        st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{record['_id']}"
                ):

                    delete_fitness_record(
                        str(record["_id"])
                    )

                    st.rerun()

else:

    st.info(
        "No fitness records added yet."
    )

