
import os
import json
import jsonref
import openai
import sys
from openai import OpenAI
# import requests
from pprint import pp

openapi_spec = {
        "paths": {
            "/users": {
                "get": {
                    "operationId": "get_users",
                    "description": "Get all users",
                    "parameters": [
                        {
                            "name": "limit",
                            "schema": {"type": "integer"}
                        }
                    ]
                },
                "post": {
                    "operationId": "create_user",
                    "description": "Create a new user",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "email": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

client = OpenAI()
def openapi_to_functions(openapi_spec):
    functions = []

    for path, methods in openapi_spec["paths"].items():
        for method, spec_with_ref in methods.items():
            # 1. Resolve JSON references.
            spec = jsonref.replace_refs(spec_with_ref)

            # 2. Extract a name for the functions.
            function_name = spec.get("operationId")

            # 3. Extract a description and parameters.
            desc = spec.get("description") or spec.get("summary", "")

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
            if params:
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                schema["properties"]["parameters"] = {
                    "type": "object",
                    "properties": param_properties,
                }

            functions.append(
                {"name": function_name, "description": desc, "parameters": schema}
            )

    return functions

openapi_spec_file = sys.argv[0]

with open(openapi_spec_file, 'r') as f:
    openapi_spec = jsonref.loads(f.read())

functions = openapi_to_functions(openapi_spec)

for function in functions:
    pp(function)
    print()
