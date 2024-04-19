import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyodide.http import open_url
from matplotlib.widgets import RadioButtons


df2000 = pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/shots-2000-preprocessed.csv"))
df2019 = pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/shots-2019-preprocessed.csv"))

court = np.array(pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/nba_court.csv"), header=None))


df_2000_ny = df2000[df2000["team"]=="New York"]
df_2019_ny = df2019[df2019["team"]=="New York"]


fig, ax = plt.subplots(1,2, figsize=(10,5))
plt.figtext(0.305, 0.005, "Reset/Undo/Redo/Pan/Zoom")

plt.subplots_adjust(left=0.2, bottom=0.4, right=0.8)
fig.canvas.set_window_title("Figure: Shot Chart Comparison between 2000 and 2019")


def shot_charts(df1, df2):
    missed1 = df1[df1["outcome"]=="missed"]
    made1 = df1[df1["outcome"]=="made"]
    ax[0].scatter(missed1["x_adj"], missed1["y_adj"], marker=".", c="red", alpha=0.35, s=8, label="missed")
    ax[0].scatter(made1["x_adj"], made1["y_adj"], marker=".", c="blue", alpha=0.35, s=8, label="made")
    ax[0].set_xlim([0,500])
    ax[0].set_ylim([0,500])
    ax[0].set_aspect("equal")
    ax[0].imshow(court, cmap="gray")
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_title("NBA 2000 Shot Chart")
    # ax[0].legend(bbox_to_anchor=(0.99,0.8), loc="upper left", handlelength=0.55)
    ax[0].legend(bbox_to_anchor=(0,0), loc="upper left", handlelength=0.55)


    # color2 = df2["outcome"].apply(lambda x: "red" if x=="missed" else "green")
    missed2 = df2[df2["outcome"]=="missed"]
    made2 = df2[df2["outcome"]=="made"]
    ax[1].scatter(missed2["x_adj"], missed2["y_adj"], marker=".", c="red", alpha=0.35, s=8, label="missed")
    ax[1].scatter(made2["x_adj"], made2["y_adj"], marker=".", c="blue", alpha=0.35, s=8, label="made")
    ax[1].set_xlim([0,500])
    ax[1].set_ylim([0,500])
    ax[1].set_aspect("equal")
    ax[1].imshow(court, cmap="gray")
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].set_title("NBA 2019 Shot Chart")




axcolor = "white"

rax2000 = plt.axes([0.025, 0.05, 0.15, 0.9], facecolor=axcolor)
teams2000 = ["All"] + sorted(list(df2000["team"].unique()))
radio2000 = RadioButtons(rax2000, teams2000, active=teams2000.index("New York"))
r = 0.015
for circ in radio2000.circles:
    circ.width = r * 2.5
    circ.height = r

plt.text(0, 1, "Team Selection 2000")

rax2019 = plt.axes([0.825, 0.05, 0.15, 0.9], facecolor=axcolor)
teams2019 = ["All"] + sorted(list(df2019["team"].unique()))
radio2019 = RadioButtons(rax2019, teams2019, active=teams2019.index("New York"))

plt.text(0, 1, "Team Selection 2019")

for circ in radio2019.circles:
    circ.width = r * 2.5
    circ.height = r

def select_team2000(val):
    df = df2000
    if val != "All":
        df = df[df["team"]==val]
    
    ax[0].cla()
    missed = df[df["outcome"]=="missed"]
    made = df[df["outcome"]=="made"]
    ax[0].scatter(missed["x_adj"], missed["y_adj"], marker=".", c="red", alpha=0.35, s=8, label="missed")
    ax[0].scatter(made["x_adj"], made["y_adj"], marker=".", c="blue", alpha=0.35, s=8, label="made")
    ax[0].set_xlim([0,500])
    ax[0].set_ylim([0,500])
    ax[0].set_aspect("equal")
    ax[0].imshow(court, cmap="gray")
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_title("NBA 2000 Shot Chart")
    # ax[0].legend(bbox_to_anchor=(0.99,0.8), loc="upper left", handlelength=0.55)
    ax[0].legend(bbox_to_anchor=(0,0), loc="upper left", handlelength=0.55)
    fig.canvas.draw_idle()

radio2000.on_clicked(select_team2000)

def select_team2019(val):
    df = df2019
    if val != "All":
        df = df[df["team"]==val]
        
    ax[1].cla()
    missed = df[df["outcome"]=="missed"]
    made = df[df["outcome"]=="made"]
    ax[1].scatter(missed["x_adj"], missed["y_adj"], marker=".", c="red", alpha=0.35, s=8, label="missed")
    ax[1].scatter(made["x_adj"], made["y_adj"], marker=".", c="blue", alpha=0.35, s=8, label="made")
    ax[1].set_xlim([0,500])
    ax[1].set_ylim([0,500])
    ax[1].set_aspect("equal")
    ax[1].imshow(court, cmap="gray")
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].set_title("NBA 2019 Shot Chart")
    fig.canvas.draw_idle()

radio2019.on_clicked(select_team2019)

shot_charts(df_2000_ny, df_2019_ny)
plt.show()