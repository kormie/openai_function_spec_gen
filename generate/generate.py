import json
import jsonref
from jsonref import JsonRef
import sys
from nodejs import npx
from pprint import pp

class Generate:

    def __init__(self: __module__, file_path: str) -> None:
        with open(file_path, 'r') as f:
            spec = jsonref.loads(f.read())

        if "swagger" in spec and spec["swagger"] == "2.0":
            print("Converting Swagger 2.0 to OpenAPI 3.0")
            openapi_spec = _convert_swagger_2_to_openapi_3(file_path)
            spec = jsonref.loads(openapi_spec)


        self.spec = spec


    def run(self: __module__, include_api_metadata: bool=False) -> list:
        functions = []
        paths_object = {}
        for path, methods in self.spec["paths"].items():
            paths_object[path] = {}
            for method, spec_with_ref in methods.items():
                print(method)
                paths_object[path][method] = _parse_method(method, spec_with_ref)
                functions.append(_parse_method(method, spec_with_ref))

        if include_api_metadata:
            response = _generate_api_metadata()
            response["paths"] = paths_object
            return response
        return functions

def _convert_swagger_2_to_openapi_3(swagger_path: str) -> str:
    completed_process = npx.run(['--yes', 'swagger2openapi', swagger_path], capture_output=True, text=True)
    return completed_process.stdout

def _parse_method(method, spec_with_ref) -> dict:
    """
    Parses the OpenAPI method specification and generates a function name, description, and parameter schema.

    Args:
        method (str): The HTTP method (e.g., GET, POST, PUT, DELETE).
        functions (list): The list of functions to append the parsed method information to.
        spec_with_ref (dict): The OpenAPI method specification with JSON references resolved.

    Returns:
        None
    """
    spec = jsonref.replace_refs(spec_with_ref)

    function_name = spec.get("operationId") or (method + "_" + spec.get("summary", ""))

    desc = spec.get("description")

    schema = {"type": "object", "properties": {}}

    req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
    if req_body:
        schema["properties"]["requestBody"] = req_body

    params = spec.get("parameters", [])
    name_additions = []

    if params:
        params = list(filter(lambda param: "in" not in param or param["in"] != "header" , params))
        param_properties = {
                    "schema": param["schema"]
                    for param in params
                    if "schema" in param
                }
        for param in params:
            if "name" in param:
                param_properties["name"] = param["name"]
        for param in params:
            if "description" in param:
                param_properties["description"] = param["description"]

        for param in params:
            if param.get("required", False):
                name = param.get("name", "").replace("_","")
                name = name[0].upper() + name[1:].replace("id", "ID")
                name_additions.append(name)

        function_name = "By".join([function_name, "And".join(name_additions)]) if name_additions else function_name

    return {"operationId": function_name, "description": desc, "parameters": params}

def _generate_api_metadata() -> dict:
    """
    Generates the OpenAPI metadata for the API.

    Args:
        spec (dict): The OpenAPI specification.

    Returns:
        dict: The OpenAPI metadata.
    """
    return {
        "openapi": "3.0.0",
        "info": {
                "title": "Test API",
                "description": "This is a test API",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": "http://localhost:3000"
                }
            ],
    }

if __name__ == '__main__':
  openapi_spec_file = sys.argv[1]
  metadata = sys.argv[2] == '-m' or False if len(sys.argv) > 2 else False


  with open(openapi_spec_file, 'r') as f:
      openapi_spec = jsonref.loads(f.read())
      spec = Generate(openapi_spec_file).run(include_api_metadata=metadata)
      print(json.dumps(spec, indent=2))
    #   pp(spec)


