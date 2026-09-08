import asyncio
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage

load_dotenv()
# for client to start the server
SERVERS = {                           #local server
    "math": {
        "transport": "stdio",
        "command": "E:/Projects/MCP_demo/.venv/Scripts/python.exe",
        "args": [
            "E:/Projects/MCP_demo/main.py"
        ]
    },
    #"remote_calculator":{             #remote server
    #    "transport": "streamable_http",
    #    "url":"https://trial-server.fastmcp.app/mcp"
    #},
    "manim-server": {
        "transport": "stdio",
        "command": "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "args": [
        "/Users/nitish/desktop/manim-mcp-server/src/manim_server.py"
      ],
        "env": {
        "MANIM_EXECUTABLE": "/Library/Frameworks/Python.framework/Versions/3.11/bin/manim"
      }
    }
    
}

async def main():
    client=MultiServerMCPClient(SERVERS)
    tools=await client.get_tools()
    
    named_tools={}
    for tool in tools:
        named_tools[tool.name]=tool
    
    print("available tools: ",named_tools.keys())
    
    #llm will identify which tool to use for the given inputs
    llm=ChatOpenAI(model='gpt-5')
    llm_with_tools=llm.bind_tools(tools)
    prompt="Draw a triangle rotating in place using the manim tool."
    response= await llm_with_tools.ainvoke(prompt)
    
    if not getattr(response, "tool_calls", None):   #if tool call not needed
        print("LLM reply:", response.content)
        return
    
    tool_messages = []             #else, return the multiple tool call info to client
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        
    final_response=await llm_with_tools.ainvoke([prompt,response,tool_messages])
    print(f"final response: {final_response.content}")
    ##now have to send this tool result to client
if __name__ == "__main__":
    asyncio.run(main())