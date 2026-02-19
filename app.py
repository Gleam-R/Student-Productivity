import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# =========================
# LOAD MODEL
# =========================
model = joblib.load("burnout_model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(page_title="AI Burnout Analyzer", layout="centered")

st.title("Student Burnout Analyzer")
st.markdown("Smart prediction based on your daily habits.")

# =========================
# INPUT SECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    deadline = st.slider("Upcoming Deadlines", 0, 10, 2)
    sleep = st.slider("Sleep Hours", 0.0, 12.0, 6.0)
    job = st.selectbox("Part Time Job", [0, 1])

with col2:
    screen = st.slider("Screen Time (hours)", 0.0, 15.0, 5.0)
    exercise = st.slider("Exercise Minutes", 0, 180, 30)
    caffeine = st.slider("Caffeine Intake (mg)", 0, 600, 100)

# =========================
# PREDICTION
# =========================
if st.button("Analyze Burnout"):

    input_data = pd.DataFrame({
        'upcoming_deadline': [deadline],
        'sleep_hours': [sleep],
        'part_time_job': [job],
        'screen_time_hours': [screen],
        'exercise_minutes': [exercise],
        'caffeine_intake_mg': [caffeine]
    })

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    burnout_value = float(prediction[0])

    st.subheader("Burnout Score")
    st.metric(label="Predicted Burnout Level", value=f"{burnout_value:.2f} / 100")

    # =========================
    # GAUGE CHART
    # =========================
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=burnout_value,
        title={'text': "Burnout Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "salmon"}
            ],
        }
    ))

    st.plotly_chart(fig)

    # =========================
    # INTERPRETATION
    # =========================
    if burnout_value < 30:
        st.success("🟢 Low Burnout — Your habits are well balanced.")
    elif burnout_value < 60:
        st.warning("🟡 Medium Burnout — Stress is accumulating.")
    else:
        st.error("🔴 High Burnout — Consider rest and stress management.")

    # =========================
    # RADAR CHART (HABIT PROFILE)
    # =========================
    st.subheader("Your Habit Profile")

    categories = [
        "Deadlines",
        "Sleep",
        "Screen Time",
        "Exercise",
        "Caffeine"
    ]

    values = [
        deadline,
        sleep,
        screen,
        exercise / 10,   # scale down
        caffeine / 50    # scale down
    ]

    radar_fig = go.Figure()

    radar_fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))

    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False
    )

    st.plotly_chart(radar_fig)

    # =========================
    # SMART INSIGHT
    # =========================
    st.subheader("Insights")

    if sleep < 8:
        st.write("• You may need more sleep.")
    if exercise < 30:
        st.write("• Increasing physical activity could reduce burnout.")
    if deadline > 6:
        st.write("• High deadline pressure detected.")
    if caffeine > 300:
        st.write("• High caffeine intake may indicate stress.")
    if deadline <= 6 and sleep >= 8 and exercise >= 30 and caffeine <= 300:
        st.write("• Your habits are generally healthy!")