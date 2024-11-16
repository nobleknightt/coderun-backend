import os
import subprocess
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

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
    exe_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".rs", mode="w", delete=False) as temp_source_file:
            temp_source_file.write(request.source)
            source_file = temp_source_file.name
        
        source_path = Path(source_file)
        exe_file = source_path.with_suffix('')

        compilation_result = subprocess.run(
            ["rustc", str(source_file), "-o", str(exe_file)], capture_output=True, text=True
        )
        
        if compilation_result.returncode != 0:
            return {"stdout": "", "stderr": compilation_result.stderr, "toast": ""}
        
        execution_result = subprocess.run(
            [str(exe_file)], input=request.stdin, capture_output=True, text=True, timeout=5,
        )
        
        if execution_result.returncode != 0:
            return {"stdout": "", "stderr": execution_result.stderr, "toast": ""}

        return {"stdout": execution_result.stdout, "stderr": "", "toast": ""}

    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "", "toast": "Programs are allowed to run for a maximum of 5 seconds."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if source_file and os.path.exists(source_file):
            os.remove(source_file)
        if exe_file and os.path.exists(exe_file):
            os.remove(exe_file)
