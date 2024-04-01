import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pyscript import display


df1 = pd.read_csv("./data/shots-2000.csv")
df2 = pd.read_csv("./data/shots-2019.csv")

def preprocess(df):
    df["x"] = df["x"].str.rstrip("px")
    df["y"] = df["y"].str.rstrip("px")
    df = df.astype({"x":"int64", "y":"int64"})
    df = df.rename({"x": "y", "y":"x"}, axis=1)
    hoop = (250, 50)
    x_offset = hoop[0] - df[df["distance"]=="0ft"]["x"].mean()
    y_offset = hoop[1] - df[df["distance"]=="0ft"]["y"].mean()
    df["x_adj"] = df["x"].apply(lambda x: x + x_offset)
    df["y_adj"] = df["y"].apply(lambda x: x + y_offset)
    return df


def filter_df(df, col, condition):
    return df[df[col] == condition]

df1 = preprocess(df1)
df2 = preprocess(df2)


df_2000_ny = filter_df(df1, "team", "New York")
df_2019_ny = filter_df(df2, "team", "New York")


filename = "./data/nba_court.png"
img = None  
try: 
    img = Image.open(filename)
except IOError:
    pass

width, height = img.size
img = img.crop((0, 0.55, width - 0.7, height))

def shot_charts(df1, df2):
    color1 = df1["outcome"].apply(lambda x: "red" if x=="missed" else "green")

    fig, ax = plt.subplots(1,2, figsize=(15,15))

    ax[0].scatter(df1["x_adj"], df1["y_adj"], marker="x", c=color1, alpha=0.5)
    ax[0].set_xlim([0,500])
    ax[0].set_ylim([0,500])
    ax[0].set_aspect("equal")
    ax[0].imshow(img)
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    ax[0].set_title("NBA 2000 Shot Chart")


    color2 = df2["outcome"].apply(lambda x: "red" if x=="missed" else "green")


    ax[1].scatter(df2["x_adj"], df2["y_adj"], marker="x", c=color2, alpha=0.5)
    ax[1].set_xlim([0,500])
    ax[1].set_ylim([0,500])
    ax[1].set_aspect("equal")
    ax[1].imshow(img)
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].set_title("NBA 2019 Shot Chart")

    plt.tight_layout()
    # plt.show()
    display(fig, target="mpl")

shot_charts(df_2000_ny, df_2019_ny)