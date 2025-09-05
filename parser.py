import json
import requests
import logging as logger
from copy import deepcopy
from typing import List
from mcp.types import Tool, TextContent

# --------------------------
# OpenAPI Parser
# --------------------------

def resolve_ref(ref: str, spec: dict):
    """Resolve a $ref like '#/components/schemas/WeatherRequest'."""
    parts = ref.lstrip("#/").split("/")
    obj = spec
    for part in parts:
        obj = obj[part]
    return deepcopy(obj)

def expand_schema(schema: dict, spec: dict):
    """Recursively expand schema by resolving $ref."""
    if not isinstance(schema, dict):
        return schema

    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], spec)

    if "properties" in schema:
        for k, v in schema["properties"].items():
            schema["properties"][k] = expand_schema(v, spec)

    if "items" in schema:
        schema["items"] = expand_schema(schema["items"], spec)

    return schema

def parse_openapi_to_tools(url: str):
    """
    Parse OpenAPI spec and return:
      1. tools (list of Tool objects)
      2. tool_map (metadata for call_tool)
    """
    response = requests.get(url)
    response.raise_for_status()
    openapi_json = response.json()
    tools = []
    tool_map = {}

    for path, methods in openapi_json.get("paths", {}).items():
        for method, details in methods.items():
            tool_name = details.get("summary", path).replace(" ", "_")

            # Default input schema
            input_schema = {"type": "object", "properties": {}, "required": []}

            # Parameters (query/path)
            for param in details.get("parameters", []):
                schema = expand_schema(param.get("schema", {}), openapi_json)
                input_schema["properties"][param["name"]] = schema
                if param.get("required", False):
                    input_schema.setdefault("required", []).append(param["name"])

            # Request Body
            request_body = details.get("requestBody")
            if request_body:
                content = request_body.get("content", {})
                if "application/json" in content:
                    schema = expand_schema(content["application/json"]["schema"], openapi_json)
                    input_schema = schema  # override with request schema

            # Register Tool
            tool = Tool(
                name=tool_name,
                inputSchema=input_schema
            )
            tools.append(tool)

            property_names = list(input_schema.get("properties", {}).keys())
            build_data = lambda args, props=property_names: {k: args.get(k) for k in props}
            print(method.upper(),build_data)

            # Store for call_tool lookup
            tool_map[tool_name] = {
                "endpoint": path.lstrip("/"),
                "method": method.upper(),
                "headers": {
                    "accept": "application/json",
                    "Content-Type": "application/json"
                },
                "build_data": build_data
            }

    return  tools,tool_map

# response = requests.get("http://localhost:8000/openapi.json")
# response.raise_for_status()
# spec = response.json()
tools,tool_map = parse_openapi_to_tools("http://localhost:8000/openapi.json")
print(tool_map)