## Features

- **Swagger to OpenAI Spec Conversion Workflow**: This repository automates the conversion of Swagger (OpenAPI) specifications into OpenAI function specifications through a dedicated GitHub Actions workflow. The workflow activates on every push to the main branch, streamlining and enhancing your productivity by automating the conversion process.

- **OpenAPI to Function Spec Script**: The `generate_openai_function_spec.py` script housed in the `scripts` directory serves as the backbone for this transformation. It extracts relevant information like operation ID, description, parameters, etc., from an OpenAPI spec and reformulates it into an OpenAI function spec. This makes interacting with APIs described in OpenAPI more effective and efficient with the help of OpenAI.

- **Testing Suite**: The repository includes a `test_generate_openai_function_spec.py` file, making sure your conversions between OpenAPI and OpenAI specifications are as accurate as possible. Testing any changes in the conversion process can assure the quality and correctness of these conversions in your workflow.

- **Example OpenAPI Specification**: The repository comes with a 'spec.json' OpenAPI Specification file. This OpenAPI spec acts as a concrete example of what your API description might look like in JSON format. This is particularly useful if you are new to OpenAPI or want to test the system with a basic, functioning OpenAPI specification right out of the box.

These features tailor this repository to be a one-stop solution for anyone looking to convert OpenAPI specifications to OpenAI function specifications, with a strong focus on testing, quality assurance, and automation.
