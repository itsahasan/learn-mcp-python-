from fastmcp import FastMCP

#Create a instance of FastMCP
mcp = FastMCP()

@mcp.tool(name="fetch_data")
def fetech_data():
    """Use this tool to fatch data from a source"""
    # Simulate fetching data from a source
    ''' You can make some API calls here or fetch data from a database '''
    return {"data": "Hello World"}

@mcp.tool(name="process")
def process(path:str):
    """ Use this tool to process the data """
    # Simulate processing the fetched data
    ''' You can perform some data transformations here '''
    return {"processed_data": "Data has been processed! at path: " + path}


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")