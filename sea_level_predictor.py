import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # 1. Import data
    df = pd.read_csv("epa-sea-level.csv")

    # 2. Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # 3. Line of best fit (all data)
    res = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])

    # Extend line to 2050
    years_extended = pd.Series(range(df["Year"].min(), 2051))
    plt.plot(
        years_extended,
        res.slope * years_extended + res.intercept,
        color="red"
    )

    # 4. Line of best fit (from year 2000)
    df_recent = df[df["Year"] >= 2000]
    res_recent = linregress(df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"])

    years_recent = pd.Series(range(2000, 2051))
    plt.plot(
        years_recent,
        res_recent.slope * years_recent + res_recent.intercept,
        color="green"
    )

    # 5. Labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")

    # 6. Save and return
    plt.savefig("sea_level_plot.png")
    return plt.gca()
