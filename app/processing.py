import logging

import numpy as np
import pandas as pd
from joblib import load
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app import app


def preprocess(data, preprocessor):
    try:
        # Import store.csv
        df_store_dtypes = {"Store": int, 
                            "StoreType": "str",
                            "Assortment": "str",
                            "PromoInterval": "str"}
        df_store = pd.read_csv("data/store.csv", dtype=df_store_dtypes)

        # Parse date column
        data['Date']  = pd.to_datetime(data['Date'])
        # Add date parameters
        data = add_date_parameters(data)

        # Reorder columns (needed for ColumnTransformer)
        data = data[['Store', 'Customers', 'Open', 'Promo',
        'StateHoliday', 'SchoolHoliday', 'saleYear', 'saleMonth',
        'saleDayOfYear', 'saleDayOfWeek', 'saleWeekOfYear']]

        # Drop Open column
        data = data.drop("Open", axis=1)

        # Join dataframes if Store exists in df_store
        if data["Store"].iloc[0] in df_store["Store"].unique():
            df = data.join(df_store.set_index('Store'), on='Store')
        # Else use computed values for df_store columns
        else:
            df = no_matching_store(data, df_store)

        # Create HasCompetition Column
        df['HasCompetition'] = df.apply(competition, axis=1)
        # Drop old competition columns
        df = df.drop(columns=["CompetitionOpenSinceMonth", "CompetitionOpenSinceYear"])

        # Create HasPromo2 Column
        df["HasPromo2"] = df.apply(promo, axis=1)
        # Drop irrelevant columns (Promo2 related, Date, Index)
        df = df.drop(columns=["Promo2", "Promo2SinceWeek", "Promo2SinceYear", "PromoInterval"])

        # Parse category columns
        df = convert_to_category(df)

        # Scale and OneHotEncode features
        data = preprocess_X(df, preprocessor)

        return data
    except:
        logging.error("Error preprocessing data.")



def add_date_parameters(dframe):
    dframe["saleYear"] = dframe.Date.dt.year
    dframe["saleMonth"] = dframe.Date.dt.month
    dframe["saleDayOfYear"] = dframe.Date.dt.dayofyear
    dframe["saleWeekOfYear"] = dframe.Date.dt.isocalendar().week
    dframe = dframe.rename(columns={"DayOfWeek": "saleDayOfWeek"})

    # Drop date column
    dframe = dframe.drop("Date", axis=1)

    return dframe

def no_matching_store(df, df_store):
    # Using the most common StoreType
    df["StoreType"] = "a"
    # Using the most common Assortment
    df["Assortment"] = "a"
    # Use the median CompetitionDistance as imputation method
    df["CompetitionDistance"] = df_store["CompetitionDistance"].median()
    # Assume NaN values for CompetitionOpenSinceMonth and CompetitionOpenSinceYear
    df["CompetitionOpenSinceMonth"] = np.nan
    df["CompetitionOpenSinceYear"] = np.nan
    # Assume not participating in Promo2, NaN values for PromoSince.. and PromoInterval Columns
    df["Promo2"] = np.nan
    df["Promo2SinceWeek"] = np.nan
    df["Promo2SinceYear"] = np.nan
    df["PromoInterval"] = np.nan

    return df

# Create function for "HasCompetition" column
def competition(c):
    compYear = int(c["CompetitionOpenSinceYear"]) if not pd.isna(c["CompetitionOpenSinceYear"]) else -1
    compMonth = int(c["CompetitionOpenSinceMonth"]) if not pd.isna(c["CompetitionOpenSinceMonth"]) else -1
    if c["saleYear"] == compYear:
        if c["saleMonth"] < compMonth:
            return 0
        else:
            return 1
    elif c["saleYear"] > compYear:
        return 1
    else:
        return 0

# Create function for 'HasPromo2' column
def promo(row):
    promoYear = int(row["Promo2SinceYear"]) if not pd.isna(row["Promo2SinceYear"]) else -1
    promoWeek = int(row["Promo2SinceWeek"]) if not pd.isna(row["Promo2SinceWeek"]) else -1
    promoMonthList = row["PromoInterval"].split(",") if not pd.isna(row["PromoInterval"]) else []
    
    # Replace month strings with integer
    monthDict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sept": 9, "Oct": 10,
                "Nov": 11, "Dec": 12}
    for idx, month in enumerate(promoMonthList):
        for k in monthDict:
            if k in month:
                promoMonthList[idx] = month.replace(k, str(monthDict[k]))
    promoMonthList = list(map(int, promoMonthList)) 
        
    if row["saleYear"] > promoYear:
        if row["saleMonth"] in promoMonthList:
            return 1
    elif row["saleYear"] == promoYear:
        if row["saleWeekOfYear"] >= promoWeek:
            if row["saleMonth"] in promoMonthList:
                return 1
    return 0    

def convert_to_category(df):
    df["StateHoliday"] = df["StateHoliday"].astype('category')
    df["StoreType"] = df["StoreType"].astype('category')
    df["Assortment"] = df["Assortment"].astype('category')
    df["SchoolHoliday"] = df["SchoolHoliday"].astype('category')
    df["HasCompetition"] = df["HasCompetition"].astype('category')
    df["HasPromo2"] = df["HasPromo2"].astype('category')
    df["Store"] = df["Store"].astype('category')

    return df

def preprocess_X(data, preprocessor):
    # encode cyclical data
    data = encode_cyclical(data, 'saleDayOfYear', 365)
    data = encode_cyclical(data, 'saleWeekOfYear', 52)

    # ColumnTransformer
    processed_data = preprocessor.transform(data)

    return processed_data

def encode_cyclical(data, col, max_val):
    data[col + '_sin'] = np.sin(2 * np.pi * data.loc[:,(col)]/max_val)
    data[col + '_cos'] = np.cos(2 * np.pi * data.loc[:,(col)]/max_val)
    data.drop(col, axis=1)
    return data
