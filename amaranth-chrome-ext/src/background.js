chrome.webNavigation.onHistoryStateUpdated.addListener(function({url}) {
    // Code should only be injected if on grubhub.com/restaurant/...
    if (url.includes('restaurant')) {
        const scriptsToInject = [
            'lib/tf.min.js',
            'src/CalorieLabel.js',
            'src/AmaranthUtil.js',
            'src/CalorieLabeller.js',
            'src/content.js',
        ];

        scriptsToInject.forEach(scriptPath => {
            chrome.tabs.executeScript(null, {
                file: scriptPath,
            });
        });

        chrome.tabs.insertCSS(null, {
            file: 'src/style.css',
        });
    }
});