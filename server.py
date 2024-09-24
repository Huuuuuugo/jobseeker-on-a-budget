from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.jobseeker.com"],  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

#TODO: add temp directories
@app.post("/")
async def parse(request: Request):
    # get html
    html_content = await request.body()

    # decode html
    html_string = html_content.decode("utf-8")

    with open('input.html', 'w') as file:
        file.write(html_string)

    subprocess.run(["python", "parser.py"])

    with open("output.html", 'r') as file:
        output = file.read()
    
    return HTMLResponse(output)