# Lint as: python3
"""This script is used to run the amaranth.ml module as an executable.

For now, this script just delegates it's main to amaranth.ml.train
"""

from amaranth.ml import train
from amaranth.ml import interactive


def main():
  # List of possible functions this module can perform
  # List elements should be tuples of str titles and functions to call
  options = [
      ('Training: Train ML model on the dataset', train.main),
      (('Interactive: Interact with the ML model by giving it strings to '
        'classify'), interactive.main),
  ]

  # Prompt user
  print('Please enter the number of the option you\'d like to choose.')
  print('---')
  for idx, (option_title, _) in enumerate(options):
    print(f'{idx}) {option_title}')

  # Parse user's input choice
  choice = None
  while choice is None:
    try:
      user_in = int(input())
      if 0 <= user_in < len(options):
        choice = user_in
      else:
        print('Please enter an option from the list above.')
    except ValueError:
      print('Please enter a valid integer.')

  # Run user's choice
  options[choice][1]()


if __name__ == '__main__':
  main()
