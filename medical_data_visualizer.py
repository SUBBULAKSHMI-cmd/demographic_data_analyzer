import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import data
df = pd.read_csv("medical_examination.csv")

# 2. Add 'overweight' column
df['height_m'] = df['height'] / 100
df['bmi'] = df['weight'] / (df['height_m'] ** 2)
df['overweight'] = (df['bmi'] > 25).astype(int)

# 3. Normalize cholesterol and gluc (0 = good, 1 = bad)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# ----------- CATEGORICAL PLOT -----------
def draw_cat_plot():
    # 4. Create DataFrame for cat plot
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 5. Group and count data
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']) \
                   .size() \
                   .reset_index(name='total')

    # 6. Draw catplot
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    ).fig

    # 7. Save figure
    fig.savefig('catplot.png')
    return fig


# ----------- HEAT MAP -----------
def draw_heat_map():
    # 8. Clean data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 9. Correlation matrix
    corr = df_heat.corr()

    # 10. Mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 11. Set up figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # 12. Draw heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # 13. Save figure
    fig.savefig('heatmap.png')
    return fig
