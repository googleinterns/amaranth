/** An object which labels a dish name as low, average, or high-calorie. */
class CalorieLabeller {
  /**
   * Creates a CalorieLabeller object.
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
    dishName = AmaranthUtil.removeSpecialCharacters(dishName).toLowerCase();
    const splitDishName = dishName.split(/\s+/);

    const tokenizedDishName = splitDishName.map((word) => {
      if (this.tokenizer_.has(word)) {
        return this.tokenizer_.get(word);
      } else {
        return this.tokenizer_.get('OOV');
      }
    });

    // Ensure tokenizedDishName.length === 43 for input into ML model. This is
    // because the number 43 was the largest input in our original dataset
    const inputLength = 43;
    const input = AmaranthUtil.padArray(tokenizedDishName, inputLength, 0)
        .slice(0, inputLength);
    const inputTensor = tf.tensor([input]);
    const calorieLabels = this.model_.predict(inputTensor);

    const [lowCalConf, avgCalConf, hiCalConf] = calorieLabels.arraySync()[0];
    const maxConfidence = Math.max(lowCalConf, avgCalConf, hiCalConf);

    if (lowCalConf == maxConfidence) {
      return CalorieLabel.LOW_CALORIE;
    } else if (avgCalConf == maxConfidence) {
      return CalorieLabel.AVERAGE_CALORIE;
    } else if (hiCalConf == maxConfidence) {
      return CalorieLabel.HIGH_CALORIE;
    }
  }
}
