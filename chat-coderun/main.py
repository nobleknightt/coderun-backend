import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return "pong"


system_message = """
You are an AI designed to answer **only programming-related questions**. If a user asks a question that is not about programming (such as general knowledge, personal advice, or other non-programming topics), reply with:

"I can only answer programming-related questions."

**Guidelines:**
- **Always** format your response in Markdown.
- Focus your responses strictly on programming languages, algorithms, data structures, software development, debugging, and other technical topics related to programming.
- For any query that is not related to programming, immediately provide the default response mentioned above.
"""


# @app.post("/chat")
# async def execute_code(request: list[dict[str, str]]):
#     try:
#         response = requests.post(
#             os.environ["URL"],
#             json={
#                 "model": os.environ["MODEL"],
#                 "messages": [{"role": "system", "content": system_message}, *request],
#                 "stream": False,  # keep false as of now
#             },
#         )
#         response = response.json()
#         return [
#             *request,
#             {"role": "assistant", "content": response["message"]["content"]},
#         ]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def execute_code(request: list[dict[str, str]]):
    try:
        response = requests.post(
            os.environ["URL"],
            headers={"Authorization": f"Bearer {os.environ['API_KEY']}"},
            json={
                "model": os.environ["MODEL"],
                "messages": [{"role": "system", "content": system_message}, *request],
                "stream": False,  # keep false as of now
            },
        )
        response = response.json()
        return [
            *request,
            {
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            },
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
