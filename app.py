import streamlit as st

st.title("AI Healthcare Assistant")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Medication Tracker", "Fitness Tracker", "Health Assistant"]
)

medicine = st.text_input("Medicine name")
dosage = st.text_input("Dosage")

if st.button("Add Medicine"):
    st.write("Medicine added successfully")


steps = st.number_input("Steps")
calories = st.number_input("Calories")

if st.button("Save Fitness Data"):
    st.write("Fitness data saved")