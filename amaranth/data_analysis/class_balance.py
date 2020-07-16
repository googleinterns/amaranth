# Lint as: python3
"""This script checks the balance of classes in the FDC dataset.

Classes are split based on LOW_CALORIE_THRESHOLD and
HIGH_CALORIE_THRESHOLD in the amaranth module.
"""

import os
import pandas as pd

import amaranth
from amaranth.ml import lib

FDC_DATA_DIR = '../../data/fdc/'


def main():
  # Read in calorie data
  current_dir = os.path.dirname(__file__)
  abs_fdc_data_dir = os.path.join(current_dir, FDC_DATA_DIR)

  food = pd.read_csv(os.path.join(abs_fdc_data_dir, 'food.csv'))
  nutrient = pd.read_csv(os.path.join(
      abs_fdc_data_dir, 'nutrient.csv')).rename(columns={'id': 'nutrient_id'})
  food_nutrient = pd.read_csv(
      os.path.join(abs_fdc_data_dir, 'food_nutrient.csv'))
  combined = lib.combine_dataframes('fdc_id', food, food_nutrient)
  combined = lib.combine_dataframes('nutrient_id', combined, nutrient)

  calorie_data = lib.get_calorie_data(combined, 'kcal')
  calorie_data = calorie_data[[
      'description', 'data_type', 'name', 'amount', 'unit_name'
  ]]  # Keep only relevant cols
  calorie_data = lib.clean_data(calorie_data)

  # Count rows with low, avg, or high calorie labels
  low_cal_cnt = 0
  avg_cal_cnt = 0
  hi_cal_cnt = 0
  for _, row in calorie_data.iterrows():
    cal = row['amount']
    if cal < amaranth.LOW_CALORIE_THRESHOLD:
      low_cal_cnt += 1
    elif cal < amaranth.HIGH_CALORIE_THRESHOLD:
      avg_cal_cnt += 1
    else:
      hi_cal_cnt += 1

  print('Class balance in FDC Dataset:')
  print(f'Low calorie:     {low_cal_cnt/len(calorie_data)}')
  print(f'Average calorie: {avg_cal_cnt/len(calorie_data)}')
  print(f'High calorie:    {hi_cal_cnt/len(calorie_data)}')


if __name__ == '__main__':
  main()
