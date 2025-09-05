from typing import Any,List
from mcp.server import Server, NotificationOptions
from mcp.types import Tool
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from mcp.server.models import InitializationOptions

import asyncio
import requests

from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.applications import Starlette
import uvicorn
from parser import parse_openapi_to_tools
port=8000
# global input_scheme

mcp=Server(
    name="sample MCP without FASTMCP"
)

import logging as logger
from mcp.types import TextContent
def register_handlers():
    @mcp.list_tools()
    async def list_tools() -> List[Tool]:
        """Return a list of tools based on the OpenAPI spec endpoints."""
        
        #
        # NEED TO IMPORT AN FUNCTION WHICH TAKES THE .json as input and Fetches
        # the endpoints Arguments, parameters into it.
        # logger.info("Listing available tools")
        # tools = []
        
        # # Create the tool definition
        # tool = Tool(
        #     name="ADD",
        #     inputSchema=input_scheme[0]
        # )
        # tool2=Tool(
        #     name='Multiply',
        #     inputSchema=input_scheme[1]
        # )
        # tool3=Tool(
        #     name="weather",
        #     inputSchema=input_scheme[2]
        # )
        
        # tools.append(tool)
        # tools.append(tool2)
        # tools.append(tool3)
        # logger.info(f"Total tools available: {len(tools)}")
        # return tools
        tools,tool_map=parse_openapi_to_tools(f"http://localhost:{port}/openapi.json")
        return tools
    # tool_config = {
    #     "ADD": {
    #         "endpoint": "add",
    #         "build_data": lambda args: {
    #             "a": args.get("a"),
    #             "b": args.get("b")
    #         }
    #     },
    #     "Multiply": {
    #         "endpoint": "multiply",
    #         "build_data": lambda args: {
    #             "a": args.get("a"),
    #             "b": args.get("b")
    #         }
    #     },
    #     "weather": {
    #         "endpoint": "get_alerts",
    #         "build_data": lambda args: {
    #             "state": args.get("state")
    #         }
    #     }
    # }
    @mcp.call_tool()
    async def call_tool(name: str, arguments: dict | None):
        try:
            # Map tool names to their corresponding endpoints
            _,tool_map=parse_openapi_to_tools(f"http://localhost:{port}/openapi.json")
            if name not in tool_map.keys():
                raise ValueError(f"Unknown tool: {name}")


            # config = tool_config[name]
            # url = f"http://localhost:{port}/{config['endpoint']}"
            print("ABOUT TO CALL THE TOOL", name)
            url = f"http://localhost:{port}/{tool_map[name]['endpoint']}"
            headers = tool_map[name]['headers']

            # data = config["build_data"](arguments or {})
            data = tool_map[name]['build_data'](arguments or {})

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            return [TextContent(type="text", text=response.text)]

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error calling tool {name}: {str(e)}")]

# Return of the Register Handlers
# For the purposes of testing, return the handlers so they can be manually invoked by tests
    return { "list_tools": list_tools, "call_tool": call_tool }

async def handle_sse(request):
  async with sse.connect_sse(
    request.scope, request.receive, request._send
  ) as streams:
    await mcp.run(
      streams[0], streams[1], InitializationOptions(
        server_name="your_server_name",
        server_version="1.0.0",  # Added missing required field
        capabilities=mcp.get_capabilities(
          notification_options=NotificationOptions(),
          experimental_capabilities={},
        ),
      )
    )
    # Return empty response to avoid NoneType error
    return Response()

async def main():
  register_handlers()

  
if __name__ =="__main__":
    # register_handlers()
    asyncio.run(main())
    sse = SseServerTransport("/messages/")

  # Create Starlette routes for SSE and message handling
    routes = [
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages/", app=sse.handle_post_message),
    ]


    starlette_app = Starlette(routes=routes)
    # starlette_app = starlette(routes=routes)
    uvicorn.run(starlette_app, host="localhost", port=8001)

    
    
# Execution Code for the
# @server.call_tool()
# async def handle_call_tool(
#     name: str, arguments: dict | None
# ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
#     # Implementation

# @server.list_resource_templates()
# async def handle_list_resource_templates() -> list[types.ResourceTemplate]:
#     # Implementation

# 3. Define notification handlers if needed:
# @server.progress_notification()
# async def handle_progress(
#     progress_token: str | int, progress: float, total: float | None,
#     message: str | None
# ) -> None:
#     # Implementation

# 4. Run the server:
# async def main():
#     async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
#         await server.run(
#             read_stream,
#             write_stream,
#             InitializationOptions(
#                 server_name="your_server_name",
#                 server_version="your_version",
#                 capabilities=server.get_capabilities(
#                     notification_options=NotificationOptions(),
#                     experimental_capabilities={},
#                 ),
#             ),
#         )

# asyncio.run(main())


