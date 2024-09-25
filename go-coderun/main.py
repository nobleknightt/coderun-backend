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
    code: str

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    source_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".go", mode="w", delete=False) as temp_file:
            temp_file.write(request.code)
            source_file = temp_file.name

        execution_result = subprocess.run(
            ["go", "run", source_file], capture_output=True, text=True
        )
        
        if execution_result.returncode != 0:
            return {"output": execution_result.stderr, "suggestion": ""}

        return {"output": execution_result.stdout, "suggestion": ""}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if source_file and os.path.exists(source_file):
            os.remove(source_file)
