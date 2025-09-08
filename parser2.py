import json
import requests
import logging as logger
from copy import deepcopy
from typing import List
from mcp.types import Tool, TextContent

def resolve_ref_2(ref: str, spec: dict):
    """Resolve a $ref like '#/definitions/WeatherRequest'."""
    parts = ref.lstrip("#/").split("/")
    obj = spec
    for part in parts:
        obj = obj[part]
    return deepcopy(obj)


def expand_schema_2(schema: dict, spec: dict):
    """Recursively expand schema by resolving $ref for Swagger 2.0."""
    if not isinstance(schema, dict):
        return schema

    if "$ref" in schema:
        schema = resolve_ref_2(schema["$ref"], spec)

    if "properties" in schema:
        for k, v in schema["properties"].items():
            schema["properties"][k] = expand_schema_2(v, spec)

    if "items" in schema:
        schema["items"] = expand_schema_2(schema["items"], spec)

    return schema


def parse_openapi_2_to_tools(url: str):
    response = requests.get(url)
    response.raise_for_status()
    swagger_json = response.json()
    tools = []
    tool_map = {}

    for path, methods in swagger_json.get("paths", {}).items():
        for method, details in methods.items():
            tool_name = details.get("summary", path).replace(" ", "_")

            input_schema = {"type": "object", "properties": {}, "required": []}

            # Parameters might include body parameters
            for param in details.get("parameters", []):
                if param.get("in") == "body":
                    # Body schema inside `schema` key in param
                    schema = expand_schema_2(param.get("schema", {}), swagger_json)
                    input_schema = schema  # override with body schema
                else:
                    # query/path/header parameters
                    schema = param.get("type", "string")
                    schema_obj = {"type": schema}
                    input_schema["properties"][param["name"]] = schema_obj
                    if param.get("required", False):
                        input_schema.setdefault("required", []).append(param["name"])

            tool = Tool(
                name=tool_name,
                inputSchema=input_schema
            )
            tools.append(tool)

            property_names = list(input_schema.get("properties", {}).keys())
            build_data = lambda args, props=property_names: {k: args.get(k) for k in props}

            tool_map[tool_name] = {
                "endpoint": path.lstrip("/"),
                "method": method.upper(),
                "headers": {
                    "accept": "application/json",
                    "Content-Type": "application/json"
                },
                "build_data": build_data
            }

    return tools, tool_map
