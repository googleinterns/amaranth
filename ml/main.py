"""TODO(tlauerman): DO NOT SUBMIT without one-line documentation for main."""

# %% define imports and functions
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np

fdc_data_dir = '../data/fdc/'


def load_calorie_data():
  """Load calorie_data from relevant csv files in FDC datatset."""
  food = pd.read_csv(fdc_data_dir + 'food.csv').set_index('fdc_id')
  nutrient = pd.read_csv(fdc_data_dir + 'nutrient.csv')
  food_nutrient = pd.read_csv(fdc_data_dir + 'food_nutrient.csv')

  # combine food & nutrient data
  combined = food.join(food_nutrient.set_index('fdc_id'))
  combined = combined.join(nutrient.set_index('id'), on='nutrient_id')

  # extract energy/kcal data
  calorie_data = combined[(combined['name'] == 'Energy')
                          & (combined['unit_name'] == 'KCAL')]
  calorie_data = calorie_data[[
      'description', 'data_type', 'name', 'amount', 'unit_name'
  ]]  # keep relevant cols
  calorie_data = calorie_data.dropna().drop_duplicates()  # clean data

  return calorie_data


def add_calorie_labels(calorie_data, low_calorie_threshold,
                       high_calorie_threshold):
  """set 'calorie_label' for each row in the dataset to reflect which class of calorie that dish falls under"""

  def label_row(calorie_data_row):
    if calorie_data_row['amount'] < low_calorie_threshold:
      return [1, 0, 0] # low calorie
    elif calorie_data_row['amount'] > high_calorie_threshold:
      return [0, 0, 1] # high calorie
    else:
      return [0, 1, 0] # avg calorie

  calorie_data['calorie_label'] = calorie_data.apply(
      lambda row: label_row(row), axis=1)

  return calorie_data


def num_unique_words(series):
  """Counts the number of unique words (space-separated) in all strings of a pandas Series."""
  words = set()
  for entry in series:
    words.update(entry.split(' +'))

  return len(words)


def max_sequence_length(series):
  """Compute the max length of the values in a pandas Series."""
  max_len = None
  for entry in series:
    if max_len is None or len(entry) > max_len:
      max_len = len(entry)

  return max_len

def add_input_labels(calorie_data, vocab_size, max_corpus_length):
  """Set 'input' for each row in the dataset to reflect the encoded input of the text."""

  def input_for_row(row):
    encoded = keras.preprocessing.text.one_hot(row['description'], vocab_size)
    
    while len(encoded) < max_corpus_length:
      encoded.append(0)

    return encoded

  calorie_data['input'] = calorie_data.apply(lambda row: input_for_row(row), axis=1)
  return calorie_data


# %% read data from disk
print(f'Tensorflow version {tf.__version__}')
calorie_data = load_calorie_data()
add_calorie_labels(calorie_data, low_calorie_threshold=100, high_calorie_threshold=500)

# %% add encode 'description' into a new 'input' column in calorie_data
calorie_data['description'] = calorie_data['description'].str.replace(',', '').str.lower()
corpus = calorie_data['description']
vocab_size = num_unique_words(corpus)
tokenized_corpus = corpus.map(lambda desc: desc.split(' '))
max_corpus_length = max_sequence_length(tokenized_corpus)
calorie_data = add_input_labels(calorie_data, vocab_size, max_corpus_length)

# %% create model
model = keras.Sequential([
  keras.layers.Embedding(vocab_size, int(vocab_size**(1/4)), input_length=max_corpus_length),
  keras.layers.Flatten(),
  keras.layers.Dense(3, activation='softmax'),
])

model.compile(
  optimizer='adam',
  loss='categorical_crossentropy',
  metrics=['categorical_accuracy']
)

# %% model stats
model.summary()
model._layers = [layer for layer in model._layers if not isinstance(layer, dict)] # workaround for bug in keras.util.plot_model
keras.utils.plot_model(model, show_layer_names=False, show_shapes=True)

# %% split dataset
train_frac = 0.6
validation_frac = 0.2
test_frac = 0.2

train_set, validation_set, test_set = np.split(
  calorie_data.sample(frac=1), # shuffle data
  [
    int(train_frac * len(calorie_data)),
    int((train_frac + validation_frac) * len(calorie_data)),
  ]
)

# %% train model
history = model.fit(
  # keras.utils.to_categorical(train_set['description'], num_classes=vocab_size),
  np.stack(train_set['input']),
  np.stack(train_set['calorie_label']),
  validation_data=(
    np.stack(validation_set['input']),
    np.stack(validation_set['calorie_label'])
  ),
  callbacks=[keras.callbacks.TensorBoard()],
)

# %% evaluate model
results = model.evaluate(
  # keras.utils.to_categorical(test_set['description'], num_classes=vocab_size),
  np.stack(test_set['input']),
  np.stack(test_set['calorie_label']),
)

print(results)

# %%
