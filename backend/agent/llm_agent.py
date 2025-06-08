# # agent/llm_agent.py

# import os
# import openai
# from agent.tools import TOOL_FUNCTIONS

# openai.api_key = os.getenv("OPENAI_API_KEY")

# tools_description = [
#     {
#         "type": "function",
#         "function": {
#             "name": "load_github_repo",
#             "description": "Fetch commits and issues from a GitHub repository.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "repo": {
#                         "type": "string",
#                         "description": "Repository name in the format owner/repo"
#                     }
#                 },
#                 "required": ["repo"]
#             }
#         }
#     }
# ]

# async def handle_user_query(text: str) -> str:
#     response = await openai.ChatCompletion.acreate(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a helpful developer assistant that can use tools to fetch project data."},
#             {"role": "user", "content": text}
#         ],
#         tools=tools_description,
#         tool_choice="auto"
#     )

#     msg = response.choices[0].message

#     if msg.tool_calls:
#         for tool_call in msg.tool_calls:
#             fn_name = tool_call.function.name
#             args = eval(tool_call.function.arguments)
#             result = TOOL_FUNCTIONS[fn_name](**args)
#             return f"✅ {fn_name} executed: {result}"
#     else:
#         return msg.content or "🤖 No action was taken."

from openai import OpenAI
import os
from agent.tools import TOOL_FUNCTIONS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def handle_user_query(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful developer assistant."},
            {"role": "user", "content": text}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "load_github_repo",
                    "description": "Fetch commits and issues from a GitHub repository.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo": {"type": "string", "description": "GitHub repo in format user/repo"}
                        },
                        "required": ["repo"]
                    }
                }
            }
        ],
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            args = eval(tool_call.function.arguments)
            result = TOOL_FUNCTIONS[fn_name](**args)
            return f"✅ {fn_name} executed: {result}"
    else:
        return msg.content or "🤖 No tool was called."
