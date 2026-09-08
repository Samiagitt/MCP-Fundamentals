from fastmcp import FastMCP
import random
import json

mcp=FastMCP("simple calculator server")

@mcp.tool
def add(a:int, b:int)-> int:
    """add two numbers together
    return the sum of a and b"""
    
    return a+b

@mcp.tool
def random_number(min_val:int=1, max_val:int=100)->int:
    """generate a random number within this range 
    between min_val and max_val
    return: A random integer between min_val and max_val"""
    return random.randint(min_val, max_val)

#resource: server information
@mcp.resource("info://server")
def server_info()->str:
    """get information about this server"""
    info={
        "name":"Simple calculator server",
        "version":"1.0.0",
        "description":"A basic MCP server with math tools",
        "tools": ["add","random_number"],
        "author": "your name"
    }
    return json.dumps(info,indent=2)


#start the server
if __name__=="__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)