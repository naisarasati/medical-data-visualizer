import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import the Data
df = pd.read_csv('/Users/macbookair/Documents/Medical-data-visualizer/medical-data-visualizer/medical_examination.csv')
print(df.head())

# 2. Create BMI Calculations
df['BMI'] = df["weight"] / ((df["height"] / 100) ** 2)

# 3. Create Condition and Column (if BMI Value > 25 = 1, else 0)
df['overweight'] = np.where((df['BMI']) > 25, 1, 0)

#4. Normalizing Data (If ('Cholesterol' or 'Gluc' == 1) = 0, else 1)
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

#5. Draw Categorical Plot
def draw_cat_plot():
    #6. Create DataFrame with Cardio as Identifier and its Variables
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    #7. Group and Count Values
    df_cat = df_cat.groupby(['variable', 'value', 'cardio']).size().reset_index(name='catplot')

    # 7. Create Categorical Plot
    sns.catplot(
        data=df_cat, 
        x='variable', 
        y='catplot', 
        hue='value', 
        col='cardio', 
        kind='bar'
    )

    # 8. Set Figure
    fig = plt.gcf()

    # 9. Call and Export Figure
    fig.savefig('catplot.png')
    return fig


# 10. Draw Heat Map 
def draw_heat_map():
    #11. Clean the Data 
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    #12. Calculate the Correleation Matrix
    corr = df_heat.corr()

    #13. Generate Mask for Upper Triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    #14. Set Figure
    fig, ax = plt.subplots(figsize=(12, 12))

    #15. Plot Matrix
    sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5}, cmap='coolwarm')

    #16. Export Plot or Figure
    fig.savefig('heatmap.png')
    return fig
