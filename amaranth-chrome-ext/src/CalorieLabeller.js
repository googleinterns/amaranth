/**
 * An object which labels a dish name as low, average, or high-calorie.
 */
class CalorieLabeller {
  /**
   * Creates a CalorieLabeller object.
   * @constructor
   * @param {Map<string, number>} tokenizer A mapping from dish name tokens to
   * unique integers
   * @param {tf.LayersModel} model Tensorflow.js layers ML model
   */
  constructor(tokenizer, model) {
    /** @private @const @type {Map<string, number>} */
    this.tokenizer_ = tokenizer;
    /** @private @const @type {tf.LayersModel} */
    this.model_ = model;
  }

  /**
   * Labels a single dish as high or low calorie.
   * @param {string} dishName The name of the dish to label
   * @return {CalorieLabel} The calorie label for the dish named dishName
   */
  label(dishName) {
    // Step 1: remove special characters from dish name
    dishName = this.removeSpecialCharacters_(dishName);

    // Step 2: convert dish name to lower case
    dishName = dishName.toLowerCase();

    // Step 3: split dish name on spaces
    const splitDishName = dishName.split(/\s+/);

    // Step 4: tokenize dish names
    const tokenizedDishName = splitDishName.map((word) => {
      if (this.tokenizer_.has(word)) {
        return this.tokenizer_.get(word);
      } else {
        // If word not present in tokenizer, return out-of-vocabulary token
        return this.tokenizer_.get('OOV');
      }
    });

    // Step 5: pad tokenized dish name to exactly length 43
    while (tokenizedDishName.length < 43) {
      tokenizedDishName.push(0);
    }
    const input = tokenizedDishName.slice(0, 43);

    // Step 5: feed dish name to ML model
    const inputTensor = tf.tensor(input);
    const calorieLabels = this.model_.predict(inputTensor);
    // Step 6: take softmax of outputs to get dish label
    // Confidence that the dish is low cal, avg cal, or high cal
    const [lowCalConf, avgCalConf, hiCalConf] = calorieLabels.arraySync();

    if (lowCalConf > avgCalConf && lowCalConf > hiCalConf) {
      // Dish is most confidently low calorie
      return CalorieLabel.LOW_CALORIE;
    } else if (avgCalConf > lowCalConf && avgCalConf > hiCalConf) {
      // Dish is most confidently average calorie
      return CalorieLabel.AVERAGE_CALORIE;
    } else if (hiCalConf > lowCalConf && hiCalConf > avgCalConf) {
      // Dish is most confidently high calorie
      return CalorieLabel.HIGH_CALORIE;
    } else {
      // If there is a tie anywhere, dish is deemed average calorie
      return CalorieLabel.AVERAGE_CALORIE;
    }
  }

  /**
   * Removes special characters from a string.
   * @private
   * @param {string} str String to remove special characters from
   * @param {string} filters Characters to remove from str
   * @return {string} `str` with all characters in `filters` removed
   */
  removeSpecialCharacters_(
      str, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n') {
    let newStr = '';
    for (const char of str) {
      if (!filters.includes(char)) {
        newStr += char;
      }
    }

    return newStr;
  }
}
