# Lint as: python3
"""This module defines helper functions for use in ml/main.py.

This module is in charge of encapsulating commonly used methods or well-defined
functions away from ml/main.py for simplicity and readability.
"""
import pandas as pd
from tensorflow import keras


def load_calorie_data(fdc_data_dir):
  """Load calorie_data from relevant csv files in FDC datatset."""
  food = pd.read_csv(fdc_data_dir + 'food.csv').set_index('fdc_id')
  nutrient = pd.read_csv(fdc_data_dir + 'nutrient.csv')
  food_nutrient = pd.read_csv(fdc_data_dir + 'food_nutrient.csv')

  # combine food & nutrient data
  combined = food.join(food_nutrient.set_index('fdc_id'))
  combined = combined.join(nutrient.set_index('id'), on='nutrient_id')

  # extract energy/kcal data
  calorie_data = combined[(combined['name'] == 'Energy')
                          & (combined['unit_name'] == 'KCAL')]
  calorie_data = calorie_data[[
      'description', 'data_type', 'name', 'amount', 'unit_name'
  ]]  # keep relevant cols
  calorie_data = calorie_data.dropna().drop_duplicates()  # clean data

  return calorie_data


def add_calorie_labels(calorie_data, low_calorie_threshold,
                       high_calorie_threshold):
  """Set 'calorie_label' for each row in the dataset to reflect which class of calorie that dish falls under."""

  def label_row(calorie_data_row):
    if calorie_data_row['amount'] < low_calorie_threshold:
      return [1, 0, 0]  # low calorie
    elif calorie_data_row['amount'] > high_calorie_threshold:
      return [0, 0, 1]  # high calorie
    else:
      return [0, 1, 0]  # avg calorie

  calorie_data['calorie_label'] = calorie_data.apply(label_row, axis=1)

  return calorie_data


def num_unique_words(series):
  """Counts the number of unique words (space-separated) in all strings of a pandas Series."""
  words = set()
  for entry in series:
    words.update(entry.split(' +'))

  return len(words)


def max_sequence_length(series):
  """Compute the max length of the values in a pandas Series."""
  max_len = None
  for entry in series:
    if max_len is None or len(entry) > max_len:
      max_len = len(entry)

  return max_len


def add_input_labels(calorie_data, vocab_size, max_corpus_length):
  """Set 'input' for each row in the dataset to reflect the encoded input of the text."""

  def input_for_row(row):
    encoded = keras.preprocessing.text.one_hot(row['description'], vocab_size)

    while len(encoded) < max_corpus_length:
      encoded.append(0)

    return encoded

  calorie_data['input'] = calorie_data.apply(input_for_row, axis=1)
  return calorie_data
