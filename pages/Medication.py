import streamlit as st
from datetime import datetime, time
from AI.assistant import (
    check_medication_interactions
)

from Utils.reminder import (
    send_medication_notification
)

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()



from Models.medication import (
    add_medication,
    get_medications,
    delete_medication,
    update_medication,
    mark_medication_taken,
    reset_daily_medications
)



st.title("💊 Medication Tracker")

reset_daily_medications(
    st.session_state["user_id"]
)

medications = get_medications(
    st.session_state["user_id"]
)
# ==========================
# ADD MEDICATION
# ==========================

st.subheader("➕ Add Medication")

medicine = st.text_input(
    "Medicine Name"
)

dosage = st.text_input(
    "Dosage"
)

med_time = st.time_input(
    "Medication Time",
    value=time(8, 0)
)

frequency = st.selectbox(
    "Frequency",
    [
        "Once Daily",
        "Twice Daily",
        "Three Times Daily",
        "Weekly"
    ]
)

time_string = med_time.strftime(
    "%H:%M"
)

if st.button(
    "➕ Add Medication",
    width="stretch"
):

    if not medicine.strip():

        st.error(
            "Medicine name is required"
        )

    elif not dosage.strip():

        st.error(
            "Dosage is required"
        )

    else:

        add_medication(
            st.session_state["user_id"],
            medicine,
            dosage,
            time_string,
            frequency
        )

        st.success(
            "Medication Added Successfully"
        )

        st.rerun()

st.divider()

# ==========================
# LOAD MEDICATIONS
# ==========================

medications = get_medications(
    st.session_state["user_id"]
)

current_time = datetime.now()

# ==========================
# STATISTICS
# ==========================

if medications:

    total_meds = len(
        medications
    )

    taken_count = len(
        [
            med
            for med in medications
            if med.get(
                "is_taken",
                False
            )
        ]
    )

    missed_count = (
        total_meds
        -
        taken_count
    )

    adherence = 0

    if total_meds > 0:

        adherence = round(
            (
                taken_count
                /
                total_meds
            ) * 100,
            1
        )

    upcoming_count = 0

    for med in medications:

        try:

            med_time_obj = datetime.strptime(
                med["time"],
                "%H:%M"
            )

            current_minutes = (
                current_time.hour * 60
                +
                current_time.minute
            )

            med_minutes = (
                med_time_obj.hour * 60
                +
                med_time_obj.minute
            )

            if (
                abs(
                    current_minutes
                    -
                    med_minutes
                ) <= 60
                and
                not med.get(
                    "is_taken",
                    False
                )
            ):

                upcoming_count += 1

        except:

            pass

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "💊 Total Medications",
        total_meds
    )

    col2.metric(
        "🚨 Upcoming",
        upcoming_count
    )

    col3.metric(
        "📅 Daily Schedule",
        total_meds
    )

    col4.metric(
        "✅ Taken",
        taken_count
    )

    col5.metric(
        "📊 Adherence",
        f"{adherence}%"
    )

st.divider()

# ==========================
# MEDICATION ALERTS
# ==========================

st.subheader(
    "🚨 Medication Alerts"
)

alerts_found = False

for med in medications:

    try:

        med_time_obj = datetime.strptime(
            med["time"],
            "%H:%M"
        )

        current_minutes = (
            current_time.hour * 60
            +
            current_time.minute
        )

        med_minutes = (
            med_time_obj.hour * 60
            +
            med_time_obj.minute
        )

        if (
             abs(
                current_minutes
                -
                med_minutes
            ) <= 30
            and
            not med.get(
                "is_taken",
                False
            )
        ):

    

            alerts_found = True

            st.warning(
                f"⏰ Time to take {med['medicine']} ({med['dosage']})"
            )

            notification_key = (
                f"notified_{med['_id']}"
            )

            if notification_key not in st.session_state:

                send_medication_notification(
                    med["medicine"],
                    med["dosage"]
                )

                st.session_state[
                    notification_key
                ] = True

    except:

        pass

if not alerts_found:

    st.info(
        "No medication reminders currently due."
    )

st.divider()

# ==========================
# SEARCH
# ==========================

search_text = st.text_input(
    "🔍 Search Medication"
)

if search_text:

    medications = [

        med

        for med in medications

        if (
            search_text.lower()
            in med.get(
                "medicine",
                ""
            ).lower()

            or

            search_text.lower()
            in med.get(
                "dosage",
                ""
            ).lower()

            or

            search_text.lower()
            in med.get(
                "frequency",
                ""
            ).lower()
        )
    ]

# ==========================
# MEDICATION LIST
# ==========================

st.subheader(
    "💊 My Medications"
)

if medications:

    for med in medications:

        with st.expander(
            f"💊 {med['medicine']} | ⏰ {med['time']} | 🔁 {med.get('frequency','Once Daily')}"
        ):

            st.info(
                f"""
Dosage: {med['dosage']}

Time: {med['time']}

Frequency: {med.get('frequency','Once Daily')}
                """
            )

            new_medicine = st.text_input(
                "Medicine",
                value=med["medicine"],
                key=f"med_{med['_id']}"
            )

            new_dosage = st.text_input(
                "Dosage",
                value=med["dosage"],
                key=f"dosage_{med['_id']}"
            )

            try:

                default_time = datetime.strptime(
                    med["time"],
                    "%H:%M"
                ).time()

            except:

                default_time = time(8, 0)

            new_time = st.time_input(
                "Medication Time",
                value=default_time,
                key=f"time_{med['_id']}"
            )

            new_time = new_time.strftime(
                "%H:%M"
            )

            frequency_options = [
                "Once Daily",
                "Twice Daily",
                "Three Times Daily",
                "Weekly"
            ]

            current_frequency = med.get(
                "frequency",
                "Once Daily"
            )

            if current_frequency not in frequency_options:

                current_frequency = (
                    "Once Daily"
                )

            new_frequency = st.selectbox(
                "Frequency",
                frequency_options,
                index=frequency_options.index(
                    current_frequency
                ),
                key=f"freq_{med['_id']}"
            )

            col1, col2, col3 = st.columns(3)

            

            with col1:

                if st.button(
                    "💾 Save Changes",
                    key=f"save_{med['_id']}",
                    width="stretch"
                ):

                    if not new_medicine.strip():

                        st.error(
                            "Medicine name is required"
                        )

                    elif not new_dosage.strip():

                        st.error(
                            "Dosage is required"
                        )   

                    else:

                        update_medication(
                            str(
                                med["_id"]
                            ),
                            new_medicine,
                            new_dosage,
                            new_time,
                            new_frequency
                        )

                        st.success(
                            "Medication Updated Successfully"
                        )

                        st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{med['_id']}",
                    width="stretch"
                ):

                    delete_medication(
                        str(
                            med["_id"]
                        )
                    )

                    st.rerun()

            with col3:

                if med.get(
                    "is_taken",
                    False
                ):

                    st.success(
                        "✅ Taken Today"
                    )

                else:

                    if st.button(
                        "✅ Mark Taken",
                        key=f"taken_{med['_id']}",
                        width="stretch"
                    ):

                        mark_medication_taken(
                            str(
                                med["_id"]
                            )
                        )

                        st.success(
                            "Medication marked as taken"
                        )

                        st.rerun()
            
else:

    st.info(
        "No medications added yet."
    )


# ==========================
# MEDICATION INTERACTION CHECKER
# ==========================

if medications:

    st.subheader(
        "🩺 Medication Safety Check"
    )

    if st.button(
        "🔍 Check Medication Interactions",
        width="stretch"
    ):

        with st.spinner(
            "Analyzing medication interactions..."
        ):

            result = (
                check_medication_interactions(
                    medications
                )
            )

        st.markdown(
            result
        )

    st.divider()