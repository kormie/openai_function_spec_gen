import pytest

from generate_openai_function_spec import openapi_to_functions

def test_openapi_to_functions():
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

    expected_functions = [
        {
            "name": "get_users",
            "description": "Get all users",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer"}
                        }
                    }
                }
            }
        },
        {
            "name": "create_user",
            "description": "Create a new user",
            "parameters": {
                "type": "object",
                "properties": {
                    "requestBody": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            }
        }
    ]

    assert openapi_to_functions(openapi_spec) == expected_functions