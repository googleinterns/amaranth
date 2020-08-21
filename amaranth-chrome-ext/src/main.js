/** The entry point of the Chrome Extension. */
async function main() {
  const mlModelPath = chrome.runtime.getURL('assets/model/model.json');
  const tokenizerPath = chrome.runtime.getURL('assets/tokenizer.json');
  const dishNameSelector = '.menuItem-name';

  // Load tokenizer dictionary
  const response = await fetch(tokenizerPath);
  const tokenizerObj = await response.json();
  const tokenizer = new Map(Object.entries(tokenizerObj));

  // Attempt to load ML model
  const model = await tf.loadLayersModel(mlModelPath);
  const labeller = new CalorieLabeller(tokenizer, model);

  // Periodically check page to see if it has fully loaded.
  // Modern web pages will often "load" in the technical sense, but often
  // display a loading animation until dishes are actually populated.
  const stateCheck = setInterval(() => {
    if (document.querySelectorAll(dishNameSelector).length > 0) {
      clearInterval(stateCheck);
      for (const dishNameElem of document.querySelectorAll(dishNameSelector)) {
        labelDish(dishNameElem, labeller);
      }
    }
  }, 100);
}

/**
 * Label a single dish as low, average, or high-calorie. This includes
 * processing in the ML model, creating the label, and adding it to the DOM.
 *
 * The calorie label element will be added as a sibling to `dishNameElem` in the
 * DOM, coming directly after it.
 * @param {Element} dishNameElem DOM element that contains the dish name
 * @param {CalorieLabeller} labeller Determines what labels to give dishes
 */
async function labelDish(dishNameElem, labeller) {
  const dishName = dishNameElem.innerHTML;
  const calorieLabel = labeller.label(dishName);

  // Create calorie label element
  const calorieLabelElem = document.createElement('p');
  calorieLabelElem.appendChild(document.createTextNode(calorieLabel));

  if (calorieLabel == CalorieLabel.LOW_CALORIE) {
    calorieLabelElem.className = 'amaranth-low-calorie';
  } else if (calorieLabel == CalorieLabel.AVERAGE_CALORIE) {
    calorieLabelElem.className = 'amaranth-average-calorie';
  } else if (calorieLabel == CalorieLabel.HIGH_CALORIE) {
    calorieLabelElem.className = 'amaranth-high-calorie';
  }

  dishNameElem.parentElement.appendChild(calorieLabelElem);
}

main();
