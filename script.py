import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the datasets
matches_path = r"C:\Users\Admin\Documents\Python\Project\csv_files\IPL_Matches.csv"
ball_data_path = r"C:\Users\Admin\Documents\Python\Project\csv_files\IPL_Ball_by_Ball.csv"

matches = pd.read_csv(matches_path)
ball_data = pd.read_csv(ball_data_path)

# Set up Streamlit page
st.set_page_config(page_title="IPL Data Analysis", layout="wide")

# Page Title
st.title("🏏 IPL Data Analysis Dashboard")

# Static Info Boxes
st.markdown("### 📊 IPL Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", matches.shape[0])
col2.metric("Total Teams", len(matches["Team1"].unique()))
col3.metric("Total Venues", len(matches["Venue"].unique()))
col4.metric("Total Seasons", len(matches["Season"].unique()))

# Top 10 Run Scorers
st.markdown("## 🔥 Top 10 Run Scorers")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Top Run Scorers")

    # Check for correct column names
    if "batter" in ball_data.columns and "batsman_run" in ball_data.columns:
        top_scorers = ball_data.groupby("batter")["batsman_run"].sum().sort_values(ascending=False).head(10)
    else:
        st.error("Column names don't match. Please check dataset structure.")
        st.stop()

    # Display Data
    for idx, (player, runs) in enumerate(top_scorers.items(), start=1):
        st.write(f"**{idx}. {player}** - {runs} runs")

with col_right:
    st.subheader("📊 Runs Scored Analysis")
    fig, ax = plt.subplots()
    top_scorers.plot(kind="bar", ax=ax, color="orange")
    ax.set_xlabel("Player")
    ax.set_ylabel("Total Runs")
    ax.set_title("Top 10 Run Scorers")
    st.pyplot(fig)

# Most Successful Team
st.markdown("## 🏆 Most Successful Team")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Winning Team Analysis")
    if "WinningTeam" in matches.columns:
        team_wins = matches["WinningTeam"].value_counts()
        best_team = team_wins.idxmax()
        st.write(f"🏅 **Most Successful Team:** {best_team}")
        st.write(f"🎯 **Total Wins:** {team_wins.max()}")
    else:
        st.error("Column 'WinningTeam' not found in dataset.")

with col2:
    st.subheader("📊 Teams with Most Wins")
    fig, ax = plt.subplots()
    team_wins.plot(kind="bar", ax=ax, color="blue")
    ax.set_xlabel("Team")
    ax.set_ylabel("Total Wins")
    ax.set_title("Top Winning Teams")
    st.pyplot(fig)

# Toss Impact Analysis
st.markdown("## 🎲 Toss Winning Impact")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Does Winning Toss Matter?")
    if "TossWinner" in matches.columns and "WinningTeam" in matches.columns:
        toss_win_match_win = matches[matches["TossWinner"] == matches["WinningTeam"]].shape[0]
        total_matches = matches.shape[0]
        win_percentage = round((toss_win_match_win / total_matches) * 100, 2)

        st.write(f"🎯 **Matches where Toss Winner also won the Match:** {toss_win_match_win}")
        st.write(f"📊 **Win Percentage:** {win_percentage}%")
    else:
        st.error("Columns 'TossWinner' and 'WinningTeam' not found in dataset.")

with col2:
    st.subheader("📊 Toss Impact Visualization")
    labels = ["Toss Winner also Won", "Toss Winner Lost"]
    values = [toss_win_match_win, total_matches - toss_win_match_win]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", colors=["green", "red"])
    ax.set_title("Toss Impact on Match Results")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("📌 *Data Source: IPL Official Records* | Developed by **Ankita Advitot** 🚀")
