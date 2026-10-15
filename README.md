# MCP stdio demo

A Python example that exposes tools through a FastMCP server and discovers them with an MCP client. The client launches the server as a subprocess and communicates over standard input and output (stdio).

## Requirements

- Python 3.14 or newer
- `uv` or `pip`

## Setup

Run these commands from the project root in PowerShell.

Using uv:

```powershell
uv sync
.\.venv\Scripts\Activate.ps1
```

Or using pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

With the environment activated, you can use either `python -m pip install <package>` or `uv pip install <package>` to install packages into it. Declare project dependencies in `pyproject.toml` to keep setup reproducible; `uv sync` uses that file and the lockfile rather than preserving arbitrary manual installs.

## Files

| File | Purpose |
| --- | --- |
| `mcpservers/1_stdio.py` | Defines the tools and runs the stdio server. |
| `mcpclients/1_stdio_client.py` | Starts the server, initializes a session, and lists its tools. |

## Run the example

```powershell
python ./mcpclients/1_stdio_client.py
```

Alternatively, run without activating the environment:

```powershell
uv run ./mcpclients/1_stdio_client.py
```

The client prints the server path followed by an `Available tools:` result containing `fetch_data` and `process`. It currently prints the complete result object, including schema and metadata. Listing tools does not execute them.

The client starts the server automatically, using the same Python interpreter through `sys.executable`. Its server path must point to `mcpservers/1_stdio.py`; pointing it to the client itself repeatedly launches more clients.

## Available tools

| Tool name | Parameters | Return value |
| --- | --- | --- |
| `fetch_data` | None | `{"data": "Hello World"}` |
| `process` | `path` (required string) | `{"processed_data": "Data has been processed! at path: <path>"}` |

Both tools return demonstration data. `process` includes the supplied path in its response; it does not read or modify a file.

The exposed name comes from the decorator:

```python
@mcp.tool(name="fetch_data")
def fetech_data():
    ...
```

Although the Python function is currently spelled `fetech_data`, clients see `fetch_data`.

## Readable tool output

To display names, descriptions, and parameters more clearly, replace the client's `list_tools()` and print statements with this code inside the initialized session:

```python
result = await session.list_tools()

print("\nAvailable tools:")
for index, tool in enumerate(result.tools, start=1):
    print(f"\n{index}. {tool.name}")
    print(f"   Description: {(tool.description or '').strip()}")

    parameters = tool.input_schema.get("properties", {})
    required = tool.input_schema.get("required", [])
    if not parameters:
        print("   Parameters: None")
    else:
        for name, schema in parameters.items():
            status = "required" if name in required else "optional"
            print(f"   - {name}: {schema.get('type', 'any')} ({status})")
```

## Call a tool

Add calls inside the initialized `ClientSession` block:

```python
data = await session.call_tool("fetch_data", arguments={})
print("Fetch result:", data)

processed = await session.call_tool(
    "process", arguments={"path": "example.txt"}
)
print("Process result:", processed)
```

## Troubleshooting

- **`read_stream and write_stream are required`:** pass the streams returned by `stdio_client` into `ClientSession(read, write)`.
- **Initialization waits without listing tools:** check that the subprocess path points to the server rather than the client.
- **Running the server alone appears to wait:** a stdio server waits for MCP messages from a client. Run the client command above for this example.
- **Protocol errors after adding server logging:** keep standard output reserved for MCP messages. Send server diagnostics to standard error.
