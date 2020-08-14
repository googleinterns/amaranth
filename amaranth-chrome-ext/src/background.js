chrome.webNavigation.onHistoryStateUpdated.addListener(function({url}) {
    // Code should only be injected if on a restaurant's page
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
    }
});