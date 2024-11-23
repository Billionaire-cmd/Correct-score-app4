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
league_avg_goals_conceded = st.sidebar.number_input("League Average Goals Conceded per Match", min_value=0.1, value=1.5, step=0.1)

# Helper Functions
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

def calculate_most_probable_scoreline(home_mean, away_mean, max_goals=5):
    max_prob = 0
    most_likely_scoreline = (0, 0)
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            prob = poisson_prob(home_mean, home_goals) * poisson_prob(away_mean, away_goals)
            if prob > max_prob:
                max_prob = prob
                most_likely_scoreline = (home_goals, away_goals)
    return most_likely_scoreline, max_prob * 100

# Calculations
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_conceded
away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
away_defense_strength = avg_away_goals_conceded / league_avg_goals_conceded

home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

# Most Probable Scoreline
most_likely_scoreline, most_likely_prob = calculate_most_probable_scoreline(home_expected_goals, away_expected_goals)

# Display Results
st.subheader("Expected Goals")
st.write(f"**Home Team Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Team Expected Goals:** {away_expected_goals:.2f}")

st.subheader("Most Likely Outcome")
st.write(
    f"The most likely scoreline is **{most_likely_scoreline[0]}-{most_likely_scoreline[1]}** "
    f"with a probability of **{most_likely_prob:.2f}%**."
)
