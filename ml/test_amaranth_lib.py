# Lint as: python3
"""These tests ensure correctness for the helper functions in amaranth_lib."""

import unittest
import ml.amaranth_lib as amaranth
import pandas as pd


class TestAmaranthHelpers(unittest.TestCase):

  def test_combine_dataframes(self):
    self.assertTrue(
        amaranth.combine_dataframes('').equals(pd.DataFrame()),
        'Combining no DataFrames yields an empty DataFrame')
    self.assertTrue(
        amaranth.combine_dataframes(
            'id', pd.DataFrame(data={
                'id': [1, 2, 3],
                'val': [4, 5, 6]
            })).equals(
                pd.DataFrame(data={
                    'id': [1, 2, 3],
                    'val': [4, 5, 6],
                }).set_index('id')),
        'Combining one DataFrame yields the same DataFrame')
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
                    }).set_index('id')),
        ('Combining two DataFrames yields one DataFrame with the properties '
         'of both'))
    with self.assertRaises(
        KeyError,
        msg=('Combining DataFrame(s) with an index that isn\'t present '
             'results in a KeyError')):
      amaranth.combine_dataframes(
          'wrong_id', pd.DataFrame(data={
              'id': [1, 2, 3],
              'val': [4, 5, 6],
          }))

  def test_get_calorie_data(self):
    with self.assertRaises(
        KeyError,
        msg=('Getting calorie data of a DataFrame without \'name\' or '
             '\'unit_name\' columns results in a KeyError')):
      amaranth.get_calorie_data(pd.DataFrame(), '')
    self.assertTrue(
        amaranth.get_calorie_data(
            pd.DataFrame(
                data={
                    'name': ['Energy', 'Energy', 'Fat'],
                    'unit_name': ['kcal', 'kj', 'kcal'],
                }), 'kcal').equals(
                    pd.DataFrame(data={
                        'name': ['Energy'],
                        'unit_name': ['kcal'],
                    })),
        ('Getting calorie data of a DataFrame should only return columns '
         'where \'name\' = \'Energy\' and \'unit_name\' = \'unit\''))

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
