import os
import subprocess
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeExecutionRequest(BaseModel):
    source: str
    stdin: str

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    source_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as temp_file:
            temp_file.write(request.source)
            source_file = temp_file.name

        result = subprocess.run(
            ["node", source_file], input=request.stdin, capture_output=True, text=True, timeout=5
        )

        if result.returncode != 0:
            return {"stdout": "", "stderr": result.stderr, "toast": ""}

        return {"stdout": result.stdout, "stderr": "", "toast": ""}

    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "", "toast": "Programs are allowed to run for a maximum of 5 seconds."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if source_file and os.path.exists(source_file):
            os.remove(source_file)
