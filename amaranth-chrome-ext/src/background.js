/** Executes the main.js file in the context of the user's current webpage. */
function injectAmaranth() {
  chrome.tabs.executeScript(null, {
    file: 'src/main.js',
  });
}

chrome.webNavigation.onCompleted.addListener(injectAmaranth, {
  // Dishes should only be analyzed on Grubhub's restaurant pages
  url: [{pathPrefix: '/restaurant'}],
});

// Due to Grubhub making use of HTML5's new pushState API, we can't rely on
// the user refreshing the webpage as a reliable trigger for the extension. The
// onHistoryStateUpdated hook listens for when a pushState call happens.
chrome.webNavigation.onHistoryStateUpdated.addListener(function() {
  // When the user navigates to a different restaurant, a new page is shown
  // for a fraction of a second. The Chrome extension labels this intermediate
  // page but not the real restaurant page when it loads. This timeout
  // attempts to avoid labelling the intermediate page.
  setTimeout(injectAmaranth, 1000);
}, {
  url: [{pathPrefix: '/restaurant'}],
});
