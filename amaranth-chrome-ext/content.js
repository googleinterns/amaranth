const tokenizerPath = chrome.runtime.getURL('tokenizer.json');

async function main() {
  // Load tokenizer dictionary
  const tokenizerResponse = await fetch(tokenizerPath);
  const tokenizerObj = await tokenizerResponse.json();
  const tokenizer = new Map(Object.entries(tokenizerObj));

  console.log(tokenizer.entries());
  console.log(tokenizer.get('bread'));
}

main();
