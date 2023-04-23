import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

TEAMS = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

CITIES = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Sharjah', 'Delhi', 'Chennai', 'Hyderabad', 'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore', 'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur']

pipe = pickle.load(open('pipe1.pkl', 'rb'))
st.title("IPL Match Winning Probability")
st.sidebar.title('IPL Win Probability Calculator')
col1, col2 = st.sidebar.columns(2)

with col1:
    batting_team = st.sidebar.selectbox('Select the batting team', sorted(TEAMS))
with col2:
    bowling_team = st.sidebar.selectbox('Select the bowling team', sorted(TEAMS))

selected_city = st.sidebar.selectbox('Select host city', sorted(CITIES))

target = st.sidebar.number_input('Target', step=1)

col3, col4, col5 = st.sidebar.columns(3)

with col3:
    score = st.number_input('Score',step=1)
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.slider('Wickets out', min_value=0, max_value=10, step=1)


if f"{batting_team}" == f"{bowling_team}":
    st.error("Batting team and Bowling team cannot be the same. Please select different teams.")
    st.stop()

if st.sidebar.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'battingteam': [batting_team],
        'bowlingteam': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets],
        'total_run_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0] * 100
    win = result[0][1] * 100
    labels = [f"{batting_team}", f"{bowling_team}"]
    colors = ['#ff6666', '#00b3b3']
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    ax.pie([loss, win], labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title("Winning Probability")
    ax.legend(title= f"Match", loc="best", bbox_to_anchor=(1, 0, 0.5, 1))
    st.subheader(f"{batting_team} vs {bowling_team}")
    st.pyplot(fig)
    st.write(f"{batting_team} has a {win:.2f}% chance of winning the match.")
    