"""This script is used to explore the FDC dataset and extract basic Calorie statistics.

Note: this file is best run as an interactive Jupyter notebook
"""

# %% import libraries
import os
import pandas as pd

# %% define constants
FDC_DATA_DIR = '../../data/fdc/'
LOW_CALORIE_THRESHOLD = 100
HIGH_CALORIE_THRESHOLD = 500

# %% read food data
current_dir = os.path.dirname(__file__)
abs_fdc_data_dir = os.path.join(current_dir, FDC_DATA_DIR)
food = pd.read_csv(os.path.join(abs_fdc_data_dir,
                                'food.csv')).set_index('fdc_id')
food.head()

# %% read nutrient data
nutrient = pd.read_csv(os.path.join(abs_fdc_data_dir, 'nutrient.csv'))
nutrient.head()

# %% read food_nutrient data
food_nutrient = pd.read_csv(os.path.join(abs_fdc_data_dir, 'food_nutrient.csv'))
food_nutrient.head()

# %% combine food & nutrient data
combined = food.join(food_nutrient.set_index('fdc_id'))
combined = combined.join(nutrient.set_index('id'), on='nutrient_id')
print(combined.columns)
combined.head()

# %% extract energy/kcal data
calData = combined[(combined['name'] == 'Energy')
                   & (combined['unit_name'] == 'KCAL')]
calData.head()

# %% clean data
calData = calData[['description', 'data_type', 'name', 'amount',
                   'unit_name']]  # keep relevant cols
calData = calData.dropna().drop_duplicates()  # clean data
print(f'{len(calData)} data points for calories')
calData.head()

# %% learn about data
calData[['amount']].describe()

# %% plot calorie distribution
calHist = calData['amount'].clip(0, 1000).hist(bins=20)
calHist.set_xlim(0, 1000)
calHist.set_xlabel('Calories (kcals per 100g of dish)')
calHist.set_ylabel('Number of Dishes')
calHist.set_title('Calorie Distribution in FDC Dataset')
calHist  # Displays histogram in Jupyter notebook. pylint: disable=pointless-statement

# %%
calKde = calData['amount'].clip(0, 1000).plot.kde()
calKde.set_xlim(0, 1000)
calKde.set_ylim(0)
calKde.set_xlabel('Calories (kcals per 100g of dish)')
calKde.set_title('Kernal Density Estimate of Calories in FDC Dataset')
calKde  # Displays plot in Jupyter notebook. pylint: disable=pointless-statement

# %% random sample of low calorie foods
print('Low calorie sample:')
calData[calData['amount'] < LOW_CALORIE_THRESHOLD].sample(10)

# %% random sample of high calorie foods
print('High calorie sample:')
calData[calData['amount'] > HIGH_CALORIE_THRESHOLD].sample(10)
