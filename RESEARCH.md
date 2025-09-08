# Documentation

#### FUTURE SCOPE

This project is a trail attempt for the `Dynamic declaration of MCP tools`
where with the decortor `@mcp.tool()` this imples and static decalrtion of the tool, where at a case, where the input(i.e for this case the return file of `URL/openapi.json`) which is a Swagger Json file for every URl the file endpoints are different, so the Static Declartion of the tool fails, where for now its needs a dynamic setup to:

1. Fetch the Endpoints and its Headers, data, arguments from swagger file
2. Automate the flow to create the List of tools `IMPLEMENTED`
3. Make logic to Call the tool `IMPLEMENTED`
4. import mcp as FASTMCP object and try doing it.
5. make a new notebook and playaround with the methods in FASTMCP, can be a groundbreaking tools if mastered.

note: `SWAGGER-MCP` is already an Existing project in the Github, and this attempt is to break through the logic behind it and host it as an SSE server and Auth and Authorization to it..

## Commit-2

Automated the Flow with Object contianed the predefined infor requested to make a Request.
the code is pretty naive, its still in the experimental setp. Code brushing is needed.

`next goal`: Beautify the Code, make a script tht can extract the header, data, input scheme from the openapi.json file.

### Making of parser

waht do i need from Parser?

- Input scheme
- Header
- endpoint (Main pripority?)
- Data

## OAS Version

Throughout the development of Swagger UI, There was multiple version releases, hence If servers were hosted long back, they might have been based on the older versions of the OAS.

Swagger UI, specifies the `OpenAPI Specifications(OAS ~ 0.1 - 3.1(current))`. So to parse the Specific version of OAS json file, there need to be an independent Parser depending on the version, coz throughout the updates, the `Key values()` in each happen to be changed.

| **OAS 2.0 JSON**                               | **OAS 3.0 JSON**                           | **Difference**                         |
| ---------------------------------------------- | ------------------------------------------ | -------------------------------------- |
| `"swagger": "2.x"`                             | `"openapi": "3.x"`                         | The version field changes.             |
| `"host"`, `"basePath"`, `"schemes"`            | `"servers": [...]`                         | Servers replace host/basePath/schemes. |
| `"definitions"`                                | `"components": { "schemas": ... }`         | Definitions moved into components.     |
| `"parameters"` (global)                        | `"components": { "parameters": ... }`      | Centralized.                           |
| `"responses"` (global)                         | `"components": { "responses": ... }`       | Centralized.                           |
| `"securityDefinitions"`                        | `"components": { "securitySchemes": ... }` | Renamed.                               |
| `"consumes"`, `"produces"`                     | `content` (per requestBody/response)       | Removed in favor of content.           |
| `paths > parameters: [ { "in": "body" ... } ]` | `paths > requestBody`                      | Body parameters replaced.              |
| N/A                                            | `"components": { "requestBodies": ... }`   | New reusable request bodies.           |
| N/A                                            | `"components": { "examples": ... }`        | Multiple named examples supported.     |
| N/A                                            | `"components": { "links": ... }`           | New (HATEOAS-style links).             |
| N/A                                            | `"components": { "callbacks": ... }`       | New (async/webhooks).                  |
| `"example"` (single)                           | `"examples"` (multiple)                    | Changed structure.                     |
| No cookie params                               | `"in": "cookie"`                           | New parameter location.                |

These were updates from OAS 2.x to 3.x, so hence the Parser need to be Tailored based on the version.

### How to Identify the OAS version?

Considering the detailed Analysis of the `openapi.json` file the key indecator to identify each were:
At the Start of the Json file the OAS version entity is always mentioned.

#### For OAS 2.0

```bash
{"swagger":"2.0","info":{"title":"FastAPI","version":"0.1.0"},"paths"
```

Later in 3.0 version of the Swagger Specification was renamed as OpenAPI specifications Adopting a Standard Naming convention.

#### For OAS 3.0

```bash
{"openapi":"3.1.0","info":{"title":"FastAPI","version":"0.1.0"},
```

With the Swagger and Openapi as the key indicator for versions, the Seperate Scripts with the `Same Output Schema` were Engineered.

```bash
OAS 2.0 Parser:  './parser2.py'

OAS 3.0 Parser:  './parser3.py'
```
