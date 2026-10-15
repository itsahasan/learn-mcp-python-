import sys
from mcp.client.stdio import stdio_client
from mcp import client, ClientSession, StdioServerParameters
from pathlib import Path
import asyncio

#Mcp server path
mcp_server_path = str(
    Path(__file__).resolve().parent.parent / "mcpservers" / "1_stdio.py"
)
print(mcp_server_path)

#Create server parameters

server_prams = StdioServerParameters(
    command=sys.executable,
    args = [str(mcp_server_path)],
    env = {}
)

#create a client session
async def main():
    async with stdio_client(server_prams) as (read, write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            #Fetch the tools
            tools = await session.list_tools()
            print("Available tools:", tools)



if __name__ == "__main__":
    asyncio.run(main())