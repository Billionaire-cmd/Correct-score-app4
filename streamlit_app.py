# Import Libraries
import streamlit as st
import numpy as np
import pandas as pd
from math import factorial  # Correct import for factorial
from scipy.stats import poisson

# Streamlit Application Title
st.title("🤖 Advanced Rabiotic Football Outcome Predictor")
st.markdown("""
Predict football match outcomes using advanced metrics like:
- **Poisson Distribution**
- **Machine Learning**
- **Odds Analysis**
- **Margin Calculations**
- **Straight Home, Draw, and Away Win**
- **Correct Score**
- **Halftime/Full-time (HT/FT)℅**
""")

# Sidebar for Input Parameters
st.sidebar.header("Input Parameters")

# Team Data Inputs
st.sidebar.subheader("Home Team")
avg_home_goals_scored = st.sidebar.number_input("Average Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_home_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Home)", min_value=0.0, value=1.2, step=0.1)

st.sidebar.subheader("Away Team")
avg_away_goals_scored = st.sidebar.number_input("Average Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)
avg_away_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Away)", min_value=0.0, value=1.3, step=0.1)

st.sidebar.subheader("League Averages")
league_avg_goals_scored = st.sidebar.number_input("League Average Goals Scored per Match", min_value=0.1, value=1.5, step=0.1)

# Helper Functions
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return [
        (i, j, home_probs[i] * away_probs[j])
        for i in range(max_goals + 1)
        for j in range(max_goals + 1)
    ]

# Calculations
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_scored
away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
away_defense_strength = avg_away_goals_conceded / league_avg_goals_scored

home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

# Display Calculations
st.subheader("Calculated Strengths")
st.write(f"**Home Attack Strength:** {home_attack_strength:.2f}")
st.write(f"**Home Defense Strength:** {home_defense_strength:.2f}")
st.write(f"**Away Attack Strength:** {away_attack_strength:.2f}")
st.write(f"**Away Defense Strength:** {away_defense_strength:.2f}")

st.subheader("Expected Goals")
st.write(f"**Home Team Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Team Expected Goals:** {away_expected_goals:.2f}")

# Predict Probabilities for Scorelines
st.subheader("Scoreline Probabilities")
max_goals = st.slider("Max Goals to Display", min_value=3, max_value=10, value=5)
probabilities = calculate_probabilities(home_expected_goals, away_expected_goals, max_goals)

# Find Most Probable Scoreline
most_likely_scoreline = max(probabilities, key=lambda x: x[2])
most_likely_prob = most_likely_scoreline[2] * 100

# Display Probabilities as Table
prob_table = pd.DataFrame(
    [(home, away, round(prob * 100, 2)) for home, away, prob in probabilities],
    columns=["Home Goals", "Away Goals", "Probability (%)"]
)
st.table(prob_table)

# Display Most Likely Outcome
st.subheader("Most Likely Outcome")
st.write(
    f"The most likely scoreline is **{most_likely_scoreline[0]}-{most_likely_scoreline[1]}** "
    f"with a probability of **{most_likely_prob:.2f}%**."
)

# Submit Button
if st.sidebar.button("Submit Prediction"):
    st.success("Prediction Submitted!")
