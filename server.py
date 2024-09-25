from tempfile import NamedTemporaryFile
import asyncio
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from parser import parse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.jobseeker.com"],  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

async def delete_file(file: str, delay: int = 5):
    await asyncio.sleep(delay)
    os.remove(file)

@app.post("/")
async def parse_html(request: Request):
    # get html
    html_content = await request.body()

    # decode html
    html_string = html_content.decode("utf-8")

    with NamedTemporaryFile(suffix='.html', dir='', mode='w+', delete=False) as input_file:
        input_file.write(html_string)

    with NamedTemporaryFile(prefix='output_', suffix='.html', dir='', mode='w+', delete=False) as output_file:
        parse(input_file.name, output_file.name)
    
    os.remove(input_file.name)
    
    asyncio.create_task(delete_file(output_file.name, 5))

    file_name_index = max(output_file.name.rfind('\\') + 1, output_file.name.rfind('/') + 1)
    file_name = output_file.name[file_name_index:]

    return HTMLResponse(file_name)

@app.get("/{file_name}")
async def show_file(file_name: str):
    if 'output_' not in file_name:
        raise HTTPException(status_code=400, detail="Invalid request!")

    return FileResponse(file_name)