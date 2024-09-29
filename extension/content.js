const API_LINK = 'https://svg-parser.onrender.com'

function requestParser() {
    cvElement = document.querySelector('div[style="position:relative"]')
    cvHtml = cvElement.outerHTML

    fetch(API_LINK,
        {
        method: 'POST',
        headers: {
            'Content-Type': 'text/html',
        },
        body: cvHtml
    })
    .then(response => response.text())
    .then(file_name => {
        window.open(`${API_LINK}/${file_name}`, '_blank')
    })
}

document.addEventListener("keydown", function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "p") {
        console.log("Printing...")
        event.preventDefault()
        requestParser()
    }
});