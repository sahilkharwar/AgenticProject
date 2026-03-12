import streamlit as st

st.title("AI Health Monitoring System")

page = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "User Profile", "Medication Tracker", "Fitness Tracker", "AI Assistant"]
)

if page == "Dashboard":

    st.header("Health Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Steps Today", "6,200", "500")
    col2.metric("Calories Burned", "350", "40")
    col3.metric("Sleep Hours", "7.5", "0.5")
elif page == "User Profile":

    st.header("Create User Profile")

    name = st.text_input("Name")
    age = st.number_input("Age")
    height = st.number_input("Height")
    weight = st.number_input("Weight")

    if st.button("Save Profile"):
        st.success("Profile saved successfully")
elif page == "Medication Tracker":

    st.header("Medication Tracker")

    medicine = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage")
    time = st.text_input("Time")

    if st.button("Add Medication"):
        st.success("Medication added")
elif page == "Fitness Tracker":

    st.header("Fitness Tracker")

    steps = st.number_input("Steps")
    calories = st.number_input("Calories")

    if st.button("Save Fitness Data"):
        st.success("Fitness data saved")
elif page == "AI Assistant":

    st.header("AI Health Assistant")

    question = st.text_input("Ask a health question")

    if st.button("Ask"):
        st.write("AI response will appear here")


import pandas as pd
import plotly.express as px

data = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Steps": [4000, 6500, 7200, 5000, 8100]
}

df = pd.DataFrame(data)

fig = px.line(df, x="Day", y="Steps", title="Weekly Step Count")

st.plotly_chart(fig)

from database import fitness_collection

fitness_data = list(fitness_collection.find())

for item in fitness_data:
    st.write(
        "Steps:", item.get("steps"),
        "Calories:", item.get("calories")
    )

from database import med_collection

st.subheader("Upcoming Medications")

meds = list(med_collection.find())

for m in meds:
    st.write(m.get("medicine"), "-", m.get("time"))
    
st.divider()
st.subheader("Fitness Trends")