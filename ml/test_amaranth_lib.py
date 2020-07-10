# Lint as: python3
"""These tests ensure correctness for the helper functions in amaranth_lib."""

import unittest
import ml.amaranth_lib as amaranth
import numpy as np
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
    self.assertTrue(
        amaranth.clean_data(
            pd.DataFrame(data={
                'id': [1, 2, 3],
                'val': ['one', 'two', 'three'],
            })).equals(
                pd.DataFrame(data={
                    'id': [1, 2, 3],
                    'val': ['one', 'two', 'three'],
                })),
        'Cleaning DataFrame without duplicates returns the same DataFrame')
    self.assertTrue(
        amaranth.clean_data(
            pd.DataFrame(data={
                'id': [1, 2],
                'val': ['one', np.nan]
            })).equals(pd.DataFrame(data={
                'id': [1],
                'val': ['one'],
            })), 'Cleaning DataFrame with NaN removes NaN')
    self.assertTrue(
        amaranth.clean_data(
            pd.DataFrame(data={
                'id': [1, 1],
                'val': ['one', 'one'],
            })).equals(pd.DataFrame(data={
                'id': [1],
                'val': ['one'],
            })), 'Cleaning DataFrame removes duplicates')
    self.assertTrue(
        amaranth.clean_data(
            pd.DataFrame(data={
                'id': [1, 2, 1],
                'val': ['one', np.nan, 'one'],
            })).equals(pd.DataFrame(data={
                'id': [1],
                'val': ['one'],
            })), 'Cleaning DataFrame removes NaN and duplicates')

  def test_add_calorie_labels(self):
    with self.assertRaises(
        KeyError,
        msg='Labelling DataFrame with no \'amount\' column raises a KeyError'):
      amaranth.add_calorie_labels(pd.DataFrame(data={'id': [1]}), 0, 0)
    self.assertTrue(
        amaranth.add_calorie_labels(
            pd.DataFrame(data={
                'amount': [0, 1, 2],
            }), 100, 200).equals(
                pd.DataFrame(
                    data={
                        'amount': [0, 1, 2],
                        'calorie_label': [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
                    })),
        'Calories are correctly labeled for low calorie dishes')
    self.assertTrue(
        amaranth.add_calorie_labels(
            pd.DataFrame(data={
                'amount': [1, 2, 3],
            }), 0, 100).equals(
                pd.DataFrame(
                    data={
                        'amount': [1, 2, 3],
                        'calorie_label': [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
                    })),
        'Calories are correctly labeled for average calorie dishes')
    self.assertTrue(
        amaranth.add_calorie_labels(
            pd.DataFrame(data={
                'amount': [1, 2, 3],
            }), 0, 0).equals(
                pd.DataFrame(
                    data={
                        'amount': [1, 2, 3],
                        'calorie_label': [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
                    })),
        'Calories are correctly labeled for high calorie dishes')
    self.assertTrue(
        amaranth.add_calorie_labels(
            pd.DataFrame(data={
                'amount': [0, 100, 200, 300, 400, 500, 600],
            }), 250, 350).equals(
                pd.DataFrame(
                    data={
                        'amount': [0, 100, 200, 300, 400, 500, 600],
                        'calorie_label': [[1, 0, 0], [1, 0, 0], [1, 0, 0],
                                          [0, 1, 0], [0, 0, 1], [0, 0, 1],
                                          [0, 0, 1]],
                    })),
        ('Calories are correctly labeled for low, average, and high calorie '
         'dishes'))

  def test_num_unique_words(self):
    self.assertEqual(
        amaranth.num_unique_words([]), 0, 'No unique words in an empty list')
    self.assertEqual(
        amaranth.num_unique_words(['one two three', 'four five six']), 6,
        'Unique words are counted across all strings in iterable')
    self.assertEqual(
        amaranth.num_unique_words(['one one two']), 2,
        'Duplicate words in the same string are not counted')
    self.assertEqual(
        amaranth.num_unique_words(['one two three', 'three four five']), 5,
        'Duplicate words in different strings are not counted')

  def test_max_sequence_length(self):
    raise NotImplementedError

  def test_add_input_labels(self):
    raise NotImplementedError


if __name__ == '__main__':
  unittest.main()
