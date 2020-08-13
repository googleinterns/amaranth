/**
 * An object which labels a dish name as low, average, or high-calorie.
 */
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
        // If word not present in tokenizer, return out-of-vocabulary token
        return this.tokenizer_.get('OOV');
      }
    });

    // Ensure tokenizedDishName.length === 43 for input into ML model
    const input = AmaranthUtil.padArray(tokenizedDishName, 43, 0).slice(0, 43);
    const inputTensor = tf.tensor([input]);
    const calorieLabels = this.model_.predict(inputTensor);

    // Confidence that the dish is low cal, avg cal, or high cal
    const [lowCalConf, avgCalConf, hiCalConf] = calorieLabels.arraySync()[0];

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
}
