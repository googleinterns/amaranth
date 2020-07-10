# Lint as: python3
"""This module defines helper functions for use in ml/main.py.

This module is in charge of encapsulating commonly used methods or well-defined
functions away from ml/main.py for simplicity and readability.
"""

from typing import Iterable, Sized
import pandas as pd
from tensorflow import keras


def combine_dataframes(index: str, *dataframes: pd.DataFrame):
  """Takes a DataFrame index, and DataFrames to join based on that index.

  Args:
    index (str): The title of the column to combine the DataFrames on
    *dataframes (pd.DataFrame): Dataframes to combine

  Returns:
    combined_dataframe (pd.DataFrame): The final combined dataframe with it's
    index set to 'index'
  Raises:
    KeyError: If any dataframes don't have the 'index' column
  """

  if not dataframes:
    return pd.DataFrame()

  combined_dataframe = dataframes[0].set_index(index)
  for df in dataframes[1:]:
    combined_dataframe = combined_dataframe.join(df.set_index(index))

  return combined_dataframe


def get_calorie_data(dataframe: pd.DataFrame, units: str):
  """Gets calorie data from a DataFrame in the specified units.

  Returns a copy of dataframe where the 'name' column must be equal to 'Energy'
  and the 'unit_name' column must be equal to 'units' (ignoring case). As such,
  both of these columns must be present, otherwise you will get a KeyError.

  Args:
    dataframe (pd.DataFrame): The DataFrame to extract calorie data from
    units (str): The desired units of the calorie data

  Returns:
    calorie_data (pd.DataFrame): All calorie-related data present in
    'dataframe' with 'units' units.

  Raises:
    KeyError: If either 'name' or 'unit_name' columns are absent in 'dataframe'
  """

  # Only keep rows where value of 'name' == 'Energy'
  calorie_data = dataframe[(dataframe['name'] == 'Energy')]
  # Only keep rows where value of 'unit_name' == units
  calorie_data = calorie_data[(
      calorie_data['unit_name'].str.lower() == units.lower())]

  return calorie_data


def clean_data(dataframe: pd.DataFrame):
  """Removes missing values and duplicate rows from a DataFrame.

  Args:
    dataframe (pd.DataFrame): The DataFrame to clean

  Returns:
    cleaned_dataframe (pd.DataFrame): The cleaned DataFrame
  """

  return dataframe.dropna().drop_duplicates()


def add_calorie_labels(calorie_data: pd.DataFrame, low_calorie_threshold: float,
                       high_calorie_threshold: float):
  """Adds a one-hot-encoded 'calorie_label' column to a calorie DataFrame.

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
  """Counts the number of unique words in an iterator of strings.

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
  """Computes the length of the longest sized element in an iterable.

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
  """One-hot-encodes a DataFrame's 'description' column into a new 'input' column.

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
