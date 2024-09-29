browser.runtime.onMessage.addEventListener((message, sender, sendResponse) => {
    if (message.action === 'fetchResource') {
        fetch(message.url)
        .then(response => response.text())
        .then(data => sendResponse({data}))
        .catch(error => sendResponse({ error: error.message }))

        return true
    }
})