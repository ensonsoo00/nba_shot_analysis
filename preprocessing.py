import pandas as pd


def parse_time(time_left, quarter, overtime):
    time_split = time_left.split(":")
    minutes = int(time_split[0])
    sec = float(time_split[1])
    total = minutes * 60 + sec
    if overtime:
        return total
    quarter_length = 12 * 60
    total += (quarter_length * (4 - quarter))
    return total
        

def preprocess(df):
    df["x"] = df["x"].str.rstrip("px").astype("int64")
    df["y"] = df["y"].str.rstrip("px").astype("int64")
    df = df.rename({"x": "y", "y":"x"}, axis=1)
    df["shots_by"] = df["play"].apply(lambda x: " ".join(str(x).split("<br>")[1].split()[:-5]))
    df["outcome"] = df["play"].apply(lambda x: str(x).split("<br>")[1].split()[-5]) 
    df["attempt"] = df["play"].apply(lambda x: str(x).split("<br>")[1].split()[-4])
    df["overtime"] = df["play"].apply(lambda x: str(x).split()[1].startswith("overtime")).astype("int32")
    df["team"] = df.apply(
        lambda x: 
        " ".join(str(x["play"]).split("<br>")[2].split()[:-3]) 
        if x["outcome"]=="made" 
        else 
        " ".join(str(x["play"]).split("<br>")[2].split()[:-2]), axis=1)
    df["winner_score"] = df.apply(
        lambda x: 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[0]) 
        if x["winner"]==x["team"] 
        else 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[1]), axis=1)
    df["loser_score"] = df.apply(
        lambda x: 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[1]) 
        if x["winner"]==x["team"] 
        else 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[0]), axis=1)
    df["team_score"] = df.apply(
        lambda x: 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[0]) 
        if x["outcome"]=="missed" 
        else 
        int(str(x["play"]).split("<br>")[2].split()[-1].split("-")[0]) - int(str(x["attempt"])[0]), axis=1)
    df["opp_score"] = df["play"].apply(lambda x: int(str(x).split("<br>")[2].split()[-1].split("-")[1]))
    df["distance"] = df["play"].apply(lambda x: int(x.split('<br>')[1].split()[-2]))
    df["time_remaining_game"] = df.apply(lambda x: parse_time(x["time_remaining"], x["quarter"], x["overtime"]), axis=1)

    
    hoop = (250, 50)
    x_offset = hoop[0] - df[df["distance"]==0]["x"].mean()
    y_offset = hoop[1] - df[df["distance"]==0]["y"].mean()
    df["x_adj"] = df["x"].apply(lambda x: x + x_offset)
    df["y_adj"] = df["y"].apply(lambda x: x + y_offset)
    return df