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
    code: str

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    source_file = None
    exe_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".rs", mode="w", delete=False) as temp_source_file:
            temp_source_file.write(request.code)
            source_file = temp_source_file.name
        
        source_path = Path(source_file)
        exe_file = source_path.with_suffix('')

        compilation_result = subprocess.run(
            ["rustc", str(source_file), "-o", str(exe_file)], capture_output=True, text=True
        )
        
        if compilation_result.returncode != 0:
            return {"output": compilation_result.stderr, "suggestion": ""}
        
        execution_result = subprocess.run(
            [str(exe_file)], capture_output=True, text=True
        )
        
        if execution_result.returncode != 0:
            return {"output": execution_result.stderr, "suggestion": ""}

        return {"output": execution_result.stdout, "suggestion": ""}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if source_file and os.path.exists(source_file):
            os.remove(source_file)
        if exe_file and os.path.exists(exe_file):
            os.remove(exe_file)
