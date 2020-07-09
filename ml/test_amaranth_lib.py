# Lint as: python3
"""These tests ensure correctness for the helper functions in amaranth_lib."""

import unittest
import ml.amaranth_lib as amaranth
import pandas as pd


class TestAmaranthHelpers(unittest.TestCase):

  def test_combine_dataframes(self):
    self.assertTrue(amaranth.combine_dataframes('').equals(pd.DataFrame()))
    self.assertTrue(
        amaranth.combine_dataframes(
            'id', pd.DataFrame(data={
                'id': [1, 2, 3],
                'val': [4, 5, 6]
            })).equals(
                pd.DataFrame(data={
                    'id': [1, 2, 3],
                    'val': [4, 5, 6],
                }).set_index('id')))
    self.assertTrue(
        amaranth.combine_dataframes(
            'id', pd.DataFrame(data={
                'id': [1, 2, 3],
                'val': [4, 5, 6],
            }),
            pd.DataFrame(data={
                'id': [1, 2, 3],
                'str': ['four', 'five', 'six'],
            })).equals(
                pd.DataFrame(
                    data={
                        'id': [1, 2, 3],
                        'val': [4, 5, 6],
                        'str': ['four', 'five', 'six'],
                    }).set_index('id')))
    with self.assertRaises(KeyError):
      amaranth.combine_dataframes(
          'wrong_id', pd.DataFrame(data={
              'id': [1, 2, 3],
              'val': [4, 5, 6],
          }))

  def test_get_calorie_data(self):
    raise NotImplementedError

  def test_clean_data(self):
    raise NotImplementedError

  def test_add_calorie_labels(self):
    raise NotImplementedError

  def test_num_unique_words(self):
    raise NotImplementedError

  def test_max_sequence_length(self):
    raise NotImplementedError

  def test_add_input_labels(self):
    raise NotImplementedError


if __name__ == '__main__':
  unittest.main()
