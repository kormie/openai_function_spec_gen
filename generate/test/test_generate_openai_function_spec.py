from generate import Generate

class TestGenerateOpenAIFunctionSpec:

    def test_openapi_to_functions(self):
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

        openapi_spec = Generate("./specs/spec.json").run()

        assert openapi_spec == expected_functions

    def test_no_operationId(self):
        openapi_spec = Generate("./specs/savings-api.json").run()

        expected_function = {
            'description': 'GetAppCards returns cards to show in app.\nCancelled cards are filtered and cards are sorted with active & primary in front.',
            'name': 'get_GetAppCardsByAccGroupID',
            'parameters': {
                'properties': {
                    'parameters': {
                        'properties': {
                            'accGroupID': {
                                'default': 'eea84cd4-5dac-470b-a42d-ef5f7e70ad5e',
                                'type': 'string'
                            }
                        },
                        'type': 'object'
                    },
                },
            'type': 'object'},
        }

        assert openapi_spec[1] == expected_function

    def test_include_api_metadata(self):
        openapi_spec = Generate("./specs/spec.json").run(include_api_metadata=True)

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

        response = {
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
            "paths": expected_functions
        }

        assert openapi_spec[0] == response