# Lint as: python3
"""This script runs the ML model in an interactive mode.

Here, you can type in any arbitrary text and the model will attempt to classify
it as a low, average, or high-calorie dish.
"""

import os

import tensorflow_addons as tfa
from tensorflow import keras

# Project resources directory
RESOURCES_DIR = '../resources/'


def main():
  current_dir = os.path.dirname(__file__)

  model = keras.models.load_model(
      os.path.join(current_dir, RESOURCES_DIR, 'model'),
      custom_objects={'F1Score': tfa.metrics.F1Score(num_classes=3)})

  print(model.summary())


if __name__ == '__main__':
  main()
