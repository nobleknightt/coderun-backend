import json
import os

import requests

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PROMPT = """You are given a source code and error message. First explain why the error occured and then suggest one and only one possible fix for it. Output should be as concise as possible and in markdown format. NO PREAMBLE.

**Source Code**
```
{source_code}
```

**Error Message**
```
{error_message}
```
"""

# rename this
def get_suggestion(source_code: str, error_message: str) -> str:

    _input = PROMPT.format(source_code=source_code, error_message=error_message)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [
                {"role": "user", "content": _input}
            ]
        })
    )

    response_json = response.json()
    output = response_json["choices"][0]["message"]["content"]

    return output
