# Lint as: python3
"""This module defines helper functions for use in ml/main.py.

This module is in charge of encapsulating commonly used methods or well-defined
functions away from ml/main.py for simplicity and readability.
"""

from typing import Iterable, Sized
import pandas as pd
from tensorflow import keras


def read_calorie_data(fdc_data_dir: str):
  """Takes a path to the FDC dataset, returns the calorie data from it.

  Args:
    fdc_data_dir (str): A path to the FDC dataset

  Returns:
    calorie_data (pd.DataFrame): All Calorie-related data from the FDC dataset
    measured in kcals
  """

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


def clean_data(dataframe: pd.DataFrame):
  """Takes a DataFrame, returns a copy of the DataFrame with missing values and duplicate rows removed.

  Args:
    dataframe (pd.DataFrame): The DataFrame to clean

  Returns:
    cleaned_dataframe (pd.DataFrame): The cleaned DataFrame
  """

  return dataframe.dropna().drop_duplicates()


def add_calorie_labels(calorie_data: pd.DataFrame, low_calorie_threshold: float,
                       high_calorie_threshold: float):
  """Adds a 'calorie_label' column to a calorie DataFrame which one-hot-encodes the calorie amount.

  Labels a calorie DataFrame by one-hot-encoding the 'amount' column into 1 of 3
  categories: low calorie, high calorie, or average calorie. The category a
  dish falls under is  determined by the low_calorie_threshold and
  high_calorie_threshold. The one-hot-encoding is added as an additional
  column titled 'calorie_label' to calorie_data and returned.

  Args:
    calorie_data (pd.DataFrame): The calorie DataFrame to label
    low_calorie_threshold (float): The boundary between low and average-calorie
      dishes
    high_calorie_threshold (float): The boundary between average and
      high-calorie dishes

  Returns:
    labeled_calorie_data (pd.DataFrame): The labeled (one-hot-encoded) DataFrame
  """

  def label_row(calorie_data_row):
    if calorie_data_row['amount'] < low_calorie_threshold:
      return [1, 0, 0]  # low calorie
    elif calorie_data_row['amount'] > high_calorie_threshold:
      return [0, 0, 1]  # high calorie
    else:
      return [0, 1, 0]  # avg calorie

  calorie_data['calorie_label'] = calorie_data.apply(label_row, axis=1)

  return calorie_data


def num_unique_words(strings: Iterable[str]):
  """Takes an iterator of strings, returns the number of unique words in all strings.

  Args:
    strings (Iterator[str]): An iterator  of strings with words separated by 1
      or more spaces

  Returns:
    word_count (int): The number of unique space-separated words in strings
  """

  words = set()

  for entry in strings:
    words.update(entry.split(' +'))

  return len(words)


def max_sequence_length(sequences: Iterable[Sized]):
  """Takes an Iterator of some sized type, returns the maximum length of all sequences.

  Args:
    sequences (Iterator): An iterator of some sized type

  Returns:
    max_len (int): The length of the longest sized type in sequences
  """
  max_len = 0
  for entry in sequences:
    if len(entry) > max_len:
      max_len = len(entry)

  return max_len


def add_input_labels(calorie_data: pd.DataFrame, vocab_size: int,
                     max_corpus_length: int):
  """Adds an 'input' column to a calorie DataFrame which one-hot-encodes the dish title.

  Creates a one-hot-encoding of the 'description' column in calorie_data. This
  one-hot-encoding is dense, where each value is the activated index in vector
  of size vocab_size. Every one-hot-encoding generated by this function will be
  of size max_corpus_length and will be added to calorie_data as a new column
  called 'input'.

  Args:
    calorie_data (pd.DataFrame): A pandas DataFrame with calorie data. Must
      include the 'description' column
    vocab_size (int): the number of unique words present in all
      calorie_data['description'] entries
    max_corpus_length (int): the maximum number of space-separated words that
      can be present in a calorie_data['description'] entry

  Returns:
    labeled_calorie_data (pd.DataFrame): The same calorie_data argument with a
    new 'input' column populated with a dense one-hot-encoding of the
    'description' column
  """

  def input_for_row(row):
    encoded = keras.preprocessing.text.one_hot(row['description'], vocab_size)

    while len(encoded) < max_corpus_length:
      encoded.append(0)

    return encoded

  calorie_data['input'] = calorie_data.apply(input_for_row, axis=1)
  return calorie_data
