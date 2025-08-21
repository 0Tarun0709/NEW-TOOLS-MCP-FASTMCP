## FUTURE SCOPE
This project is a trail attempt for the `Dynamic declaration of MCP tools`
where with the decortor `@mcp.tool()` this imples and static decalrtion of the tool, where at a case, where the input(i.e for this case the return file of `URL/openapi.json`) which is a Swagger Json file for every URl the file endpoints are different, so the Static Declartion of the tool fails, where for now its needs a dynamic setup to:
1. Fetch the Endpoints and its Headers, data, arguments from swagger file
2. Automate the flow to create the List of tools `IMPLEMENTED`
3. Make logic to Call the tool `IMPLEMENTED`
4. import mcp as FASTMCP object and try doing it.
5. make a new notebook and playaround with the methods in FASTMCP, can be a groundbreaking tools if mastered.

note: `SWAGGER-MCP` is already an Existing project in the Github, and this attempt is to break through the logic behind it and host it as an SSE server and Auth and Authorization to it..