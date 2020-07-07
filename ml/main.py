# Lint as: python3
"""This script is used to import data and build/train a nutrient-prediction ML model."""

# %% define imports and functions
import amaranth_lib as amaranth
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

FDC_DATA_DIR = '../data/fdc/'
LOW_CALORIE_THRESHOLD = 100
HIGH_CALORIE_THRESHOLD = 500


def main():
  # %% read data from disk
  print(f'Tensorflow version {tf.__version__}')
  calorie_data = amaranth.load_calorie_data(FDC_DATA_DIR)
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
  train_frac = 0.6
  validation_frac = 0.2
  test_frac = 0.2

  train_set, validation_set, test_set = np.split(
      calorie_data.sample(frac=1),  # shuffle data
      [
          int(train_frac * len(calorie_data)),
          int((train_frac + validation_frac) * len(calorie_data)),
      ])

  # %% train model
  history = model.fit(
      np.stack(train_set['input']),
      np.stack(train_set['calorie_label']),
      validation_data=(np.stack(validation_set['input']),
                       np.stack(validation_set['calorie_label'])),
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
