# Lint as: python3
"""This script is used to build and train a nutrient-prediction ML model."""

# Define imports and constants
import os
import json
import numpy as np
import pandas as pd
import sklearn.model_selection
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import text

import amaranth
from amaranth.ml import lib

# Directories to write files to
FDC_DATA_DIR = '../../data/fdc/'  # Data set directory
MODEL_IMG_DIR = '../../docs/img/'  # Model image directory
RESOURCES_DIR = '../resources/'  # Project resources directory
CHROME_EXT_DIR = 'amaranth-chrome-ext/'  # Chrome extension directory
# Fraction of data that should be used for training, validation, and testing.
# Should all sum to 1.0.
TRAIN_FRAC = 0.6
VALIDATION_FRAC = 0.2
TEST_FRAC = 0.2
# Times a token needs to appear to be in model's vocab
MIN_TOKEN_APPEARANCE = 0
# Chars to remove from dish names
DISH_NAME_FILTERS = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'


def main():
  print(f'Tensorflow version {tf.__version__}')

  # Get data directory path
  current_dir = os.path.dirname(__file__)
  abs_fdc_data_dir = os.path.join(current_dir, FDC_DATA_DIR)

  # Read data from disk
  food = pd.read_csv(os.path.join(abs_fdc_data_dir, 'food.csv'))
  nutrient = pd.read_csv(os.path.join(
      abs_fdc_data_dir, 'nutrient.csv')).rename(columns={'id': 'nutrient_id'})
  food_nutrient = pd.read_csv(
      os.path.join(abs_fdc_data_dir, 'food_nutrient.csv'))
  combined = lib.combine_dataframes('fdc_id', food, food_nutrient)
  combined = lib.combine_dataframes('nutrient_id', combined, nutrient)

  # Extract and format calorie data
  calorie_data = lib.get_calorie_data(combined, 'kcal')
  calorie_data = calorie_data[[
      'description', 'data_type', 'name', 'amount', 'unit_name'
  ]]  # Keep only relevant cols
  calorie_data = lib.clean_data(calorie_data)
  lib.add_calorie_labels(
      calorie_data,
      low_calorie_threshold=amaranth.LOW_CALORIE_THRESHOLD,
      high_calorie_threshold=amaranth.HIGH_CALORIE_THRESHOLD)

  # Normalize input strings
  # Step 1: convert strings to lowercase
  # Step 2: filter out characters present in DISH_NAME_FILTERS
  # Step 3: re-combine characters back to a normal string
  calorie_data['description'] = calorie_data['description'].apply(
      lambda desc: desc.lower(),  # Step 1
  ).apply(
      lambda desc: [char for char in desc
                    if char not in DISH_NAME_FILTERS],  # Step 2
  ).apply(
      ''.join,  #Step 3
  )

  # Do some preprocessing and calculations for encoding
  corpus = calorie_data['description']
  vocab_size = lib.num_unique_words(corpus)
  tokenized_corpus = corpus.map(lambda desc: desc.split(' '))
  max_corpus_length = lib.max_sequence_length(tokenized_corpus)

  # Encode 'description' into new column 'input'
  calorie_data['tokenized'] = calorie_data.apply(
      lambda row: text.one_hot(row['description'], vocab_size), axis=1)

  # Create tokenizer to encode input text
  tokenizer = dict()  # Dictionary mapping each unique word to a unique int
  tokenizer_cnt = dict()  # Counts appearances of each word in tokenizer
  for _, row in calorie_data.iterrows():
    for idx, word in enumerate(row['description'].split()):
      tokenizer[word] = row['tokenized'][idx]

      if word in tokenizer_cnt:
        tokenizer_cnt[word] += 1
      else:
        tokenizer_cnt[word] = 1

  # Only 'remember' words that appear at least 3 times
  for word, cnt in tokenizer_cnt.items():
    if cnt < MIN_TOKEN_APPEARANCE:
      del tokenizer[word]

  # The empty string denotes words that are OOV (out-of-vocabulary)
  # It is equal to vocab_size because all values in the tokenizer should be less
  # than vocab_size
  tokenizer[''] = 0

  json.dump(
      tokenizer,
      open(os.path.join(CHROME_EXT_DIR, 'tokenizer.json'), 'w'),
      separators=(',', ':'))

  calorie_data['input'] = calorie_data.apply(
      lambda row: [
          tokenizer[token] if token in tokenizer else tokenizer['']
          for token in row['description'].split()
      ],
      axis=1)

  # Pad 'input' column to all be the same length for embedding input
  calorie_data['input'] = calorie_data.apply(
      lambda row: lib.pad_list(row['input'], max_corpus_length, 0), axis=1)

  # Create model
  model = keras.Sequential([
      keras.layers.Embedding(
          vocab_size, int(vocab_size**(1 / 4)), input_length=max_corpus_length),
      keras.layers.Flatten(),
      keras.layers.Dense(32, activation='sigmoid'),
      keras.layers.Dense(10, activation='sigmoid'),
      keras.layers.Dense(3, activation='softmax'),
  ])

  model.compile(
      optimizer='adam',
      loss='categorical_crossentropy',
      metrics=[
          'categorical_accuracy',
          keras.metrics.Precision(),
          keras.metrics.Recall(),
      ])

  # Model stats
  model.summary()
  model._layers = [  # Workaround for bug in keras.util.plot_model pylint: disable=protected-access
      layer for layer in model._layers if not isinstance(layer, dict)  # pylint: disable=protected-access
  ]
  keras.utils.plot_model(
      model,
      to_file=os.path.join(current_dir, MODEL_IMG_DIR, 'model.png'),
      show_layer_names=False,
      show_shapes=True)

  # Split dataset
  train_set, test_set = sklearn.model_selection.train_test_split(
      calorie_data,
      train_size=TRAIN_FRAC + VALIDATION_FRAC,
      test_size=TEST_FRAC)

  # Train model
  model.fit(
      np.stack(train_set['input']),
      np.stack(train_set['calorie_label']),
      epochs=10,
      validation_split=VALIDATION_FRAC / (TRAIN_FRAC + VALIDATION_FRAC),
      callbacks=[keras.callbacks.TensorBoard()],
  )

  # Evaluate model
  results = model.evaluate(
      np.stack(test_set['input']),
      np.stack(test_set['calorie_label']),
  )

  print('\nResults:')
  print(results)

  # Save test set predictions, generate confusion matrix
  predictions = model.predict(np.stack(test_set['input']))
  predictions = tf.argmax(predictions, axis=-1)

  confusion = tf.math.confusion_matrix(
      tf.argmax(np.stack(test_set['calorie_label']), axis=-1), predictions)

  print('\nConfusion matrix')
  print('x-axis: prediction')
  print('y-axis: actual value')
  print(confusion)

  # Save model to file
  model.save(os.path.join(current_dir, RESOURCES_DIR, 'model'))


if __name__ == '__main__':
  main()
