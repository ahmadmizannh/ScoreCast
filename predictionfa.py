
import pandas as pd
#%%
clean_data_fa_cup = pd.read_csv('data\clean_data_cl.csv')
#%%
df_home = clean_data_fa_cup[['home_team', 'HomeGoals', 'AwayGoals']]
df_away = clean_data_fa_cup[['away_team', 'HomeGoals', 'AwayGoals']]

df_home = df_home.rename(columns={'home_team': 'club', 'HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'away_team': 'club', 'HomeGoals': 'GoalsConceded', 'AwayGoals': 'GoalsScored'})

df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['club']).mean()

#%%
df_team_strength
#%%
import streamlit as st
import numpy as np
from scipy.stats import poisson

# Get average goals scored and conceded for each team
team_stats = df_team_strength[['GoalsScored', 'GoalsConceded']].values

# Streamlit app
st.title("Football Match Scoreline Prediction")

# User input for home and away teams
home_team = st.text_input("Enter the home team:")
away_team = st.text_input("Enter the away team:")

# Find the respective team's statistics
home_stats = team_stats[df_team_strength.index == home_team][0] if home_team in df_team_strength.index else None
away_stats = team_stats[df_team_strength.index == away_team][0] if away_team in df_team_strength.index else None

if home_stats is not None and away_stats is not None:
    # Calculate the expected goals for each team
    lambda_home = home_stats[0] * away_stats[1] / df_team_strength['GoalsConceded'].mean()
    lambda_away = away_stats[0] * home_stats[1] / df_team_strength['GoalsConceded'].mean()

    # Predict probabilities of different scorelines
    scorelines = [(i, j) for i in range(8) for j in range(8)]
    probabilities = [poisson.pmf(score[0], lambda_home) * poisson.pmf(score[1], lambda_away) for score in scorelines]
    probabilities = np.array(probabilities).reshape((8, 8))

    # Get the most likely scoreline
    max_prob_index = np.argmax(probabilities)
    most_likely_score = scorelines[max_prob_index]

    # Display the most likely scoreline
    st.subheader("Most likely scoreline:")
    st.write(f"{home_team} {most_likely_score[0]} - {most_likely_score[1]} {away_team}")
else:
    st.write("Invalid team names. Please enter valid team names.")
