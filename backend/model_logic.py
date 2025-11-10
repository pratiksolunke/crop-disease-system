import pandas as pd
from datetime import datetime

def load_data(path="Crops_Stage_Disease_Days_Sowing_to_Harvest.csv"):
    df = pd.read_csv(path, encoding='latin1')
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.rename(columns={
        list(df.columns)[0]: "crop_name",
        list(df.columns)[1]: "days_from_sowing_start",
        list(df.columns)[2]: "crop_stage",
        list(df.columns)[3]: "crop_disease"
    }, inplace=True)
    return df

def predict_stage_and_disease(crop_name, sowing_date, df):
    sowing_date = datetime.strptime(sowing_date, "%Y-%m-%d")
    days_since = (datetime.now() - sowing_date).days
    crop_df = df[df["crop_name"].str.lower() == crop_name.lower()].sort_values("days_from_sowing_start")
    stage_row = crop_df[crop_df["days_from_sowing_start"] <= days_since].tail(1)
    if stage_row.empty:
        return {"stage": "Unknown", "diseases": []}
    stage = stage_row["crop_stage"].values[0]
    diseases = crop_df[crop_df["crop_stage"] == stage]["crop_disease"].unique().tolist()
    return {"days_since": days_since, "stage": stage, "diseases": diseases}
