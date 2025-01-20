import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize # Replacing with percentile
from scipy.stats import trim_mean # Calculate the Trimmed mean by removing X% from both tails

outliers = []
def detect_outliers_iqr(data):
    data = sorted(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    # print(q1, q3)
    IQR = q3-q1
    lwr_bound = q1-(1.5*IQR)
    upr_bound = q3+(1.5*IQR)
    # print(lwr_bound, upr_bound)
    for i in data:
        if (i<lwr_bound or i>upr_bound):
            outliers.append(i)
    return outliers# Driver code

def remove_outliers_df(df, columns=None, threshold=1.5):
    """
    Remove outliers de um DataFrame usando o método IQR.

    Args:
        df: DataFrame.
        columns: Lista de colunas para analisar. Se None, analisa todas as colunas numéricas.
        threshold: Multiplicador do IQR para definir os limites.

    Returns:
        DataFrame sem outliers.
    """

    if columns is None:
        columns = df.select_dtypes(include=['number']).columns

    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        df = df[~((df[column] < lower_bound) | (df[column] > upper_bound))]

    return df