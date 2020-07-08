# Lint as: python3
"""This script is used to import data and build/train a nutrient-prediction ML model."""

# %% define imports and constants
import amaranth_lib as amaranth
import numpy as np
import sklearn.model_selection
import tensorflow as tf
from tensorflow import keras

# Location of source data set
FDC_DATA_DIR = '../data/fdc/'

# Thresholds for what defines "high" and "low" calorie
LOW_CALORIE_THRESHOLD = 100
HIGH_CALORIE_THRESHOLD = 500

# Fraction of data that should be used for training, validation, and testing.
# Should all sum to 1.0.
TRAIN_FRAC = 0.6
VALIDATION_FRAC = 0.2
TEST_FRAC = 0.2


def main():
  # %% read data from disk
  print(f'Tensorflow version {tf.__version__}')
  calorie_data = amaranth.read_calorie_data(FDC_DATA_DIR)
  calorie_data = calorie_data[[
      'description', 'data_type', 'name', 'amount', 'unit_name'
  ]]  # keep only relevant cols
  calorie_data = amaranth.clean_data(calorie_data)
  amaranth.add_calorie_labels(
      calorie_data,
      low_calorie_threshold=LOW_CALORIE_THRESHOLD,
      high_calorie_threshold=HIGH_CALORIE_THRESHOLD)

  # %% add encode 'description' into a new 'input' column in calorie_data
  calorie_data['description'] = calorie_data['description'].str.replace(
      ',', '').str.lower()
  corpus = calorie_data['description']
  vocab_size = amaranth.num_unique_words(corpus)
  tokenized_corpus = corpus.map(lambda desc: desc.split(' '))
  max_corpus_length = amaranth.max_sequence_length(tokenized_corpus)
  calorie_data = amaranth.add_input_labels(calorie_data, vocab_size,
                                           max_corpus_length)

  # %% create model
  model = keras.Sequential([
      keras.layers.Embedding(
          vocab_size, int(vocab_size**(1 / 4)), input_length=max_corpus_length),
      keras.layers.Flatten(),
      keras.layers.Dense(3, activation='softmax'),
  ])

  model.compile(
      optimizer='adam',
      loss='categorical_crossentropy',
      metrics=[
          'categorical_accuracy',
          keras.metrics.Precision(),
          keras.metrics.Recall()
      ])

  # %% model stats
  model.summary()
  model._layers = [  # workaround for bug in keras.util.plot_model pylint: disable=protected-access
      layer for layer in model._layers if not isinstance(layer, dict)  # pylint: disable=protected-access
  ]
  keras.utils.plot_model(model, show_layer_names=False, show_shapes=True)

  # %% split dataset
  train_set, test_set = sklearn.model_selection.train_test_split(
      calorie_data,
      train_size=TRAIN_FRAC + VALIDATION_FRAC,
      test_size=TEST_FRAC)

  # %% train model
  model.fit(
      np.stack(train_set['input']),
      np.stack(train_set['calorie_label']),
      validation_split=VALIDATION_FRAC / (TRAIN_FRAC + VALIDATION_FRAC),
      callbacks=[keras.callbacks.TensorBoard()],
  )

  # %% evaluate model
  results = model.evaluate(
      np.stack(test_set['input']),
      np.stack(test_set['calorie_label']),
  )

  print(results)

  # %%


if __name__ == '__main__':
  main()
