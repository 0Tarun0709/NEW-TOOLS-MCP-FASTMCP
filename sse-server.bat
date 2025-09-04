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
# global input_scheme
input_scheme=[
    {
        "type": "object",
            "properties": {
            "a": {"type": "integer", "description": "First integer to add"},
            "b": {"type": "integer", "description": "Second integer to add"}
            },
            "required": ["a", "b"]
    },
    {
        "type": "object",
            "properties": {
            "a": {"type": "integer", "description": "First integer to Multiply"},
            "b": {"type": "integer", "description": "Second integer to Multiply"}
            },
        
            "required": ["a", "b"]
        
    }
]

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
        logger.info("Listing available tools")
        tools = []
        

            # Skip deprecated endpoints
            # Add logic to extract details from OPENAPI swagger json file
            
        # Create input schema from the endpoint's combined parameter schema
        # input_schema = {
        #     "type": "object",
        #     "properties": {
        #     "a": {"type": "integer", "description": "First integer to add"},
        #     "b": {"type": "integer", "description": "Second integer to add"}
        #     },
        #     "required": ["a", "b"]
        # }
        
        # Create the tool definition
        tool = Tool(
            name="ADD",
            inputSchema=input_scheme[0]
        )
        tool2=Tool(
            name='Multiply',
            inputSchema=input_scheme[1]
        )
        tools.append(tool)
        tools.append(tool2)
        logger.info(f"Total tools available: {len(tools)}")
        return tools

    @mcp.call_tool()
    async def call_tool(name: str, arguments: dict | None):
        try:
            if name == 'ADD':
                url = "http://localhost:8000/add"  # Replace with your endpoint URL
                data = {
                    'a': arguments.get('a', 100),
                    'b': arguments.get('b', 100)
                }
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, json=data, headers=headers)
                return [TextContent(type="text", text=response.text)]
            if name == 'Multiply':
                url = "http://localhost:8000/multiply"  # Replace with your endpoint URL
                data = {
                    'a': arguments.get('a', 100),
                    'b': arguments.get('b', 100)
                }
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, json=data, headers=headers)
                return [TextContent(type="text", text=response.text)]
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error calling tool {name}: {str(e)}")]

                
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            # error_trace = traceback.format_exc()
            # logger.error(f"Traceback: {error_trace}")
            return f'[TextContent(type="text", text=f"Error calling tool {name}: {str(e)}\n")]'

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
    # async with stdio_server() as (read_stream, write_stream):
    #     await mcp.run(
    #         read_stream,
    #         write_stream,
    #         InitializationOptions(
    #             server_name="your_server_name",
    #             server_version="your_version",
    #             capabilities=mcp.get_capabilities(
    #                 notification_options=NotificationOptions(),
    #                 experimental_capabilities={},
    #             ),
    #         ),
    #     )
  
if __name__ =="__main__":
    # register_handlers()
    asyncio.run(main())
    sse = SseServerTransport("/messages/")

  # Create Starlette routes for SSE and message handling
    routes = [
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages/", app=sse.handle_post_message),
    ]

    # Define handler functions

    # Create and run Starlette app
     # Create and run Starlette app
    starlette_app = Starlette(routes=routes)
    # starlette_app = starlette(routes=routes)
    uvicorn.run(starlette_app, host="localhost", port=8001)

    
    

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


