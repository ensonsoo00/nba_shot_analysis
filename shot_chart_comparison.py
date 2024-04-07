import pandas as pd
import matplotlib.pyplot as plt
from pyscript import display
import numpy as np
from pyodide.http import open_url
from matplotlib.widgets import RadioButtons


df2000 = pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/shots-2000-preprocessed.csv"))
df2019 = pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/shots-2019-preprocessed.csv"))

court = np.array(pd.read_csv(open_url("https://raw.githubusercontent.com/ensonsoo00/nba_shot_analysis/main/data/nba_court.csv"), header=None))


df_2000_ny = df2000[df2000["team"]=="New York"]
df_2019_ny = df2019[df2019["team"]=="New York"]


fig, ax = plt.subplots(1,2, figsize=(10,10))
plt.subplots_adjust(left=0.25, bottom=0.25, right=0.75)
def shot_charts(df1, df2):
    color1 = df1["outcome"].apply(lambda x: "red" if x=="missed" else "green")

    

    ax[0].scatter(df1["x_adj"], df1["y_adj"], marker=".", c=color1, alpha=0.5, s=5)
    ax[0].set_xlim([0,500])
    ax[0].set_ylim([0,500])
    ax[0].set_aspect("equal")
    ax[0].imshow(court, cmap="gray")
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    ax[0].set_title("NBA 2000 Shot Chart")


    color2 = df2["outcome"].apply(lambda x: "red" if x=="missed" else "green")


    ax[1].scatter(df2["x_adj"], df2["y_adj"], marker=".", c=color2, alpha=0.5, s=5)
    ax[1].set_xlim([0,500])
    ax[1].set_ylim([0,500])
    ax[1].set_aspect("equal")
    ax[1].imshow(court, cmap="gray")
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].set_title("NBA 2019 Shot Chart")

    # display(fig, target="mpl")

axcolor = "white"

rax2000 = plt.axes([0.025, 0.25, 0.15, 0.5], facecolor=axcolor)
teams2000 = ["All"] + sorted(list(df2000["team"].unique()))
radio2000 = RadioButtons(rax2000, teams2000, active=teams2000.index("New York"))
r = 0.015
for circ in radio2000.circles:
    circ.width = r * 2.5
    circ.height = r

rax2019 = plt.axes([0.825, 0.25, 0.15, 0.5], facecolor=axcolor)
teams2019 = ["All"] + sorted(list(df2019["team"].unique()))
radio2019 = RadioButtons(rax2019, teams2019, active=teams2019.index("New York"))

for circ in radio2019.circles:
    circ.width = r * 2.5
    circ.height = r

def select_team2000(val):
    df = df2000
    if val != "All":
        df = df[df["team"]==val]
    color2 = df["outcome"].apply(lambda x: "red" if x=="missed" else "green")

    ax[0].cla()
    ax[0].scatter(df["x_adj"], df["y_adj"], marker=".", c=color2, alpha=0.5, s=5)
    ax[0].set_xlim([0,500])
    ax[0].set_ylim([0,500])
    ax[0].set_aspect("equal")
    ax[0].imshow(court, cmap="gray")
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_title("NBA 2000 Shot Chart")
    fig.canvas.draw_idle()

radio2000.on_clicked(select_team2000)

def select_team2019(val):
    df = df2019
    if val != "All":
        df = df[df["team"]==val]
    color2 = df["outcome"].apply(lambda x: "red" if x=="missed" else "green")

    ax[1].cla()
    ax[1].scatter(df["x_adj"], df["y_adj"], marker=".", c=color2, alpha=0.5, s=5)
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
# display(fig, target="mpl")