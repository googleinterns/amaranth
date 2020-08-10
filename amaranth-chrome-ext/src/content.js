const mlModelPath = chrome.runtime.getURL('assets/model/model.json');
const tokenizerPath = chrome.runtime.getURL('assets/tokenizer.json');

async function main() {
  // Load tokenizer dictionary
  const response = await fetch(tokenizerPath);
  const tokenizerObj = await response.json();
  const tokenizer = new Map(Object.entries(tokenizerObj));

  console.log(tokenizer.entries());
  console.log(`Tokenizer dict size: ${tokenizer.size}`);

  // Attempt to load ML model
  const model = await tf.loadLayersModel(mlModelPath);
  console.log(model.summary());
}

main();
