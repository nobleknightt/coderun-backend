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

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    try: 
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
            temp_file.write(request.code)
            source_file = temp_file.name

        result = subprocess.run(
            ["python", source_file], capture_output=True, text=True
        )

        if result.returncode == 0:
            return {"output": result.stdout}
        else:
            return {"output": result.stderr}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if source_file:
            os.remove(source_file)
