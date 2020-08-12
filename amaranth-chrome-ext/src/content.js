const mlModelPath = chrome.runtime.getURL('assets/model/model.json');
const tokenizerPath = chrome.runtime.getURL('assets/tokenizer.json');

/** The entry point of the Chrome Extension. */
async function main() {
  // Load tokenizer dictionary
  const response = await fetch(tokenizerPath);
  const tokenizerObj = await response.json();
  const tokenizer = new Map(Object.entries(tokenizerObj));

  // Attempt to load ML model
  const model = await tf.loadLayersModel(mlModelPath);
}

main();
