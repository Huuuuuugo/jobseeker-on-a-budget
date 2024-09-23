function openNewWindow(html) {
    const newWindow = window.open(); // Open a new window
    if (newWindow) {
        newWindow.document.write(html); // Write the HTML content
        newWindow.document.close(); // Close the document to render it
        newWindow.onload = function() {
            newWindow.print()
        }
    } else {
        console.error("Failed to open new window.")
    }
}

function requestParser() {
    cvElement = document.querySelector('div[style="position:relative"]')
    cvHtml = cvElement.outerHTML

    let outputHtml = ''

    fetch('https://svg-parser.onrender.com',
        {
        method: 'POST',
        headers: {
            'Content-Type': 'text/html',
        },
        body: cvHtml
    })
    .then(response => response.text())
    .then(responseHtml => {
        outputHtml = responseHtml
        openNewWindow(outputHtml)
    })
}

document.addEventListener("keydown", function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "p") {
        console.log("Printing...")
        event.preventDefault()
        requestParser()
    }
});