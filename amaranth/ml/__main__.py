# Lint as: python3
"""This script is used to run the amaranth.ml module as an executable.

For now, this script just delegates it's main to amaranth.ml.train
"""

from amaranth.ml import train


def main():
  train.main()


if __name__ == '__main__':
  main()
