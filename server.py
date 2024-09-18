from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess


app = FastAPI()

#TODO: add temp directories
@app.post("/")
async def parse(request: Request):
    # get html
    html_content = await request.body()

    # decode html
    html_string = html_content.decode("utf-8")

    with open('input.html', 'w') as file:
        file.write(html_string.replace('\n', ''))

    subprocess.run(["python", "parser.py"])

    with open("output.html", 'r') as file:
        output = file.read()
    
    return HTMLResponse(output)