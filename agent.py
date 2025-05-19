import openai
from pipeline.config import OLLAMA_API_BASE, OLLAMA_MODEL
from tools import search_documents

openai.api_base = OLLAMA_API_BASE
openai.api_key = "ollama"  # dummy for Ollama

tool_schema = {
    "name": "search_documents",
    "description": "Search government documents containing a keyword",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {"type": "string", "description": "The keyword to search"}
        },
        "required": ["keyword"]
    }
}

async def call_agent(query: str):
    response = await openai.ChatCompletion.acreate(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": query}],
        tools=[{"type": "function", "function": tool_schema}],
        tool_choice="auto"
    )

    message = response.choices[0].message
    # print("Message:", message) # Debugging line
    
    if message.get("tool_calls"):
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = eval(tool_call.function.arguments)
        
        if function_name == "search_documents":
            result = await search_documents(arguments["keyword"])
            followup = await openai.ChatCompletion.acreate(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "user", "content": query},
                    {"role": "assistant", "tool_calls": response.choices[0].message.tool_calls},
                    {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)}
                ]
            )
            return followup.choices[0].message.content
    return message.content
