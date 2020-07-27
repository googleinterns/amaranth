# Lint as: python3
"""This script runs the ML model in an interactive mode.

Here, you can type in any arbitrary text and the model will attempt to classify
it as a low, average, or high-calorie dish.
"""

import sys
import os

import tensorflow as tf
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

  print('\nPress CTRL-D to end.')

  end = False
  while not end:
    print('\nPlease enter a dish name: ')
    dish_name = sys.stdin.readline()

    if dish_name:
      prediction, = model.predict([dish_name])
      cal_label = tf.math.argmax(prediction)

      if cal_label == 0:
        print('Low Calorie')
      elif cal_label == 1:
        print('Average Calorie')
      else:
        print('High Calorie')

      print('----------')

      low_cal_prob, avg_cal_prob, hi_cal_prob = prediction
      print('Confidence:')
      print(f'Low calorie     {low_cal_prob}')
      print(f'Average calorie {avg_cal_prob}')
      print(f'High calorie    {hi_cal_prob}')
    else:
      end = True


if __name__ == '__main__':
  main()
